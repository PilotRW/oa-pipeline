from pydantic import BaseModel

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query, Response
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.ingestion.parser import parse_file
from app.models.supplier import Supplier
from app.services.import_commit_service import (
    ImportSupplierNotFoundError,
    commit_import_draft,
)
from app.services.import_draft_service import (
    apply_import_filters,
    consume_import_draft,
    create_import_draft,
    get_import_draft,
    serialize_import_draft,
)
from app.services.import_preview_service import (
    apply_saved_filter_profile,
    build_import_dataframe_from_content,
    content_hash,
    dataframe_hash,
    export_filename,
    normalize_import_dataframe,
    search_dataframe,
    spreadsheet_safe_csv,
)
from app.services.supplier_price_service import (
    SupplierPriceDownloadError,
    download_supplier_price,
)

router = APIRouter()


class ImportCommitRequest(BaseModel):
    import_token: str
    filters: dict | None = None


class ImportFilterPreviewRequest(BaseModel):
    import_token: str
    filters: dict | None = None


class ImportPreviewExportRequest(BaseModel):
    import_token: str
    filters: dict | None = None


class ImportPreviewSearchRequest(BaseModel):
    import_token: str
    query: str
    filters: dict | None = None
    limit: int = 100


async def build_import_dataframe(file: UploadFile):
    try:
        df = await parse_file(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        return normalize_import_dataframe(df)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/upload/preview")
async def preview_upload(
    supplier_name: str = Query(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
):
    df, original_columns, normalization_report = await build_import_dataframe(file)
    supplier_result = await session.execute(
        select(Supplier).where(
            func.lower(Supplier.name) == supplier_name.strip().lower()
        )
    )
    supplier = supplier_result.scalar_one_or_none()

    draft = create_import_draft(
        supplier_name=supplier_name,
        supplier_id=supplier.id if supplier else None,
        filename=file.filename,
        df=df,
        original_columns=original_columns,
        normalization_report=normalization_report,
    )

    return apply_saved_filter_profile(
        draft=draft,
        filters=(
            supplier.import_filter_profile
            if supplier
            else None
        ),
    )


@router.post("/upload/supplier-price-preview")
async def preview_supplier_price_url(
    supplier_id: int = Query(..., ge=1),
    apply_saved_filters: bool = Query(default=False),
    session: AsyncSession = Depends(get_db),
):
    supplier = await session.get(Supplier, supplier_id)

    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    if not supplier.price_url:
        raise HTTPException(
            status_code=400,
            detail="Supplier price URL is not configured",
        )

    try:
        content, filename, metadata = await download_supplier_price(
            supplier.price_url
        )
        (
            df,
            original_columns,
            normalization_report,
        ) = build_import_dataframe_from_content(
            content=content,
            filename=filename,
        )
    except (SupplierPriceDownloadError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    file_hash = content_hash(content)
    data_hash = dataframe_hash(df)
    previous_file_hash = supplier.price_file_hash
    previous_data_hash = supplier.price_data_hash
    changed = (
        previous_file_hash is not None
        and (
            previous_file_hash != file_hash
            or previous_data_hash != data_hash
        )
    )
    draft = create_import_draft(
        supplier_name=supplier.name,
        supplier_id=supplier.id,
        filename=filename,
        df=df,
        original_columns=original_columns,
        normalization_report=normalization_report,
    )
    draft["price_tracking"] = {
        "etag": metadata.get("etag"),
        "last_modified": metadata.get("last_modified"),
        "content_length": metadata.get("content_length") or len(content),
        "file_hash": file_hash,
        "data_hash": data_hash,
        "filename": filename,
        "changed": changed or previous_file_hash is None,
    }

    result = apply_saved_filter_profile(
        draft=draft,
        filters=(
            supplier.import_filter_profile
            if apply_saved_filters
            else None
        ),
    )
    result["has_saved_import_filters"] = bool(supplier.import_filter_profile)
    result["saved_filters_applied"] = bool(
        apply_saved_filters and supplier.import_filter_profile
    )
    result["price_change_detected"] = changed
    result["price_file_hash"] = file_hash
    result["price_data_hash"] = data_hash

    return result


@router.post("/upload/commit")
async def commit_upload(
    payload: ImportCommitRequest,
    session: AsyncSession = Depends(get_db),
):
    draft = consume_import_draft(payload.import_token)

    if not draft:
        raise HTTPException(
            status_code=404,
            detail="Import preview expired or was already saved",
        )

    filters = (
        payload.filters
        if payload.filters is not None
        else draft.get("confirmed_filters")
    )
    df, filter_summary = apply_import_filters(
        draft["df"],
        filters,
    )

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="Selected filters excluded all rows",
        )

    try:
        return await commit_import_draft(
            session=session,
            supplier_name=draft["supplier_name"],
            supplier_id=draft.get("supplier_id"),
            filename=draft["filename"],
            df=df,
            original_columns=draft["original_columns"],
            normalization_report=draft["normalization_report"],
            filter_summary=filter_summary,
            price_tracking=draft.get("price_tracking"),
        )
    except ImportSupplierNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/upload/filter-preview")
async def preview_import_filters(
    payload: ImportFilterPreviewRequest,
    session: AsyncSession = Depends(get_db),
):
    draft = get_import_draft(payload.import_token)

    if not draft:
        raise HTTPException(
            status_code=404,
            detail="Import preview expired or was already saved",
        )

    df, filter_summary = apply_import_filters(
        draft["df"],
        payload.filters,
    )

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="Selected filters excluded all rows",
        )

    preview_draft = {
        **draft,
        "df": df,
        "filter_summary": filter_summary,
    }
    normalized_filters = filter_summary["filters"]
    draft["confirmed_filters"] = normalized_filters
    draft["filter_summary"] = filter_summary

    supplier_id = draft.get("supplier_id")

    if supplier_id is not None:
        supplier = await session.get(Supplier, supplier_id)

        if supplier is not None:
            supplier.import_filter_profile = normalized_filters
            await session.commit()

    return serialize_import_draft(preview_draft)


@router.post("/upload/export-preview")
async def export_import_preview(
    payload: ImportPreviewExportRequest,
):
    draft = get_import_draft(payload.import_token)

    if not draft:
        raise HTTPException(
            status_code=404,
            detail="Import preview expired or was already saved",
        )

    filters = (
        payload.filters
        if payload.filters is not None
        else draft.get("confirmed_filters")
    )
    df, _filter_summary = apply_import_filters(
        draft["df"],
        filters,
    )

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="Selected filters excluded all rows",
        )

    filename = export_filename(
        f"{draft['supplier_name']}-{draft['filename']}-preview"
    )

    return Response(
        content=spreadsheet_safe_csv(df),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}.csv"',
        },
    )


@router.post("/upload/search-preview")
async def search_import_preview(
    payload: ImportPreviewSearchRequest,
):
    draft = get_import_draft(payload.import_token)

    if not draft:
        raise HTTPException(
            status_code=404,
            detail="Import preview expired or was already saved",
        )

    filters = (
        payload.filters
        if payload.filters is not None
        else draft.get("confirmed_filters")
    )
    df, _filter_summary = apply_import_filters(
        draft["df"],
        filters,
    )

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="Selected filters excluded all rows",
        )

    try:
        return search_dataframe(
            df=df,
            query=payload.query,
            limit=payload.limit,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/upload")
async def upload_csv(
    supplier_name: str = Query(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
):
    df, original_columns, normalization_report = await build_import_dataframe(file)

    return await commit_import_draft(
        session=session,
        supplier_name=supplier_name,
        supplier_id=None,
        filename=file.filename,
        df=df,
        original_columns=original_columns,
        normalization_report=normalization_report,
    )
