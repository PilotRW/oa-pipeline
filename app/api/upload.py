import hashlib
from datetime import datetime, timezone

from pydantic import BaseModel

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query, Response
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.ingestion.parser import parse_content, parse_file
from app.ingestion.normalizer import normalize_columns
from app.ingestion.cleaners import clean_dataframe
from app.models.supplier import Supplier
from app.services.ingestion_service import (
    get_or_create_supplier,
    save_ingestion_run,
    save_column_mappings,
)
from app.services.config_service import ConfigService
from app.services.import_draft_service import (
    apply_import_filters,
    build_filter_suggestions,
    build_quality_report,
    consume_import_draft,
    create_import_draft,
    get_import_draft,
    serialize_import_draft,
)
from app.services.marketplace import currency_for_marketplace
from app.services.supplier_offer_service import save_supplier_offers
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


def export_filename(value: str) -> str:
    safe = "".join(
        character.lower() if character.isalnum() else "-"
        for character in value
    )
    safe = "-".join(part for part in safe.split("-") if part)

    return safe or "import-preview"


def spreadsheet_safe_csv(df) -> bytes:
    export_df = df.copy()
    text_identifier_columns = {
        "ean",
        "gtin",
        "upc",
        "barcode",
    }

    for column in export_df.columns:
        if str(column).strip().lower() not in text_identifier_columns:
            continue

        export_df[column] = export_df[column].apply(
            lambda value: f'="{value}"' if str(value).strip() else ""
        )

    return export_df.to_csv(index=False).encode("utf-8-sig")


def dataframe_hash(df) -> str:
    canonical = df.fillna("").to_csv(
        index=False,
        lineterminator="\n",
    )
    return hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()


async def build_import_dataframe(file: UploadFile):
    try:
        df = await parse_file(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file contains no rows")

    original_columns = list(df.columns)

    df, normalization_report = normalize_columns(df)

    df = clean_dataframe(df)

    return df, original_columns, normalization_report


def build_import_dataframe_from_content(
    content: bytes,
    filename: str,
):
    df = parse_content(
        content=content,
        filename=filename,
    )

    if df.empty:
        raise ValueError("Uploaded file contains no rows")

    original_columns = list(df.columns)
    df, normalization_report = normalize_columns(df)
    df = clean_dataframe(df)

    return df, original_columns, normalization_report


def apply_saved_filter_profile(
    draft: dict,
    filters: dict | None,
) -> dict:
    if not filters:
        return serialize_import_draft(draft)

    df, filter_summary = apply_import_filters(
        draft["df"],
        filters,
    )

    if df.empty:
        return {
            **serialize_import_draft(draft),
            "saved_filter_warning": (
                "Saved supplier filters excluded all rows and were not applied"
            ),
        }

    draft["confirmed_filters"] = filter_summary["filters"]
    draft["filter_summary"] = filter_summary

    return serialize_import_draft(
        {
            **draft,
            "df": df,
            "filter_summary": filter_summary,
        }
    )


async def commit_import_draft(
    *,
    session: AsyncSession,
    supplier_name: str,
    supplier_id: int | None,
    filename: str,
    df,
    original_columns: list,
    normalization_report: list[dict],
    filter_summary: dict | None = None,
):
    settings = await ConfigService(
        session
    ).get_pipeline_settings()

    supplier = (
        await session.get(Supplier, supplier_id)
        if supplier_id is not None
        else None
    )

    if supplier_id is not None and supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Configured supplier no longer exists",
        )

    if supplier is None:
        supplier = await get_or_create_supplier(
            session=session,
            supplier_name=supplier_name,
        )

    rows_total = len(df)
    rows_valid = len(df)
    rows_failed = 0

    ingestion_run = await save_ingestion_run(
        session=session,
        supplier_id=supplier.id,
        filename=filename,
        rows_total=rows_total,
        rows_valid=rows_valid,
        rows_failed=rows_failed,
        normalization_report=normalization_report,
    )

    mappings_saved = await save_column_mappings(
        session=session,
        supplier_id=supplier.id,
        normalization_report=normalization_report,
    )

    offers_saved = await save_supplier_offers(
        session=session,
        supplier_id=supplier.id,
        df=df,
        currency=currency_for_marketplace(settings.default_marketplace),
    )

    await session.commit()

    return {
        "supplier": {
            "id": supplier.id,
            "name": supplier.name,
        },
        "ingestion_run": {
            "id": ingestion_run.id,
            "status": ingestion_run.status,
        },
        "filename": filename,
        "rows": rows_total,
        "rows_valid": rows_valid,
        "rows_failed": rows_failed,
        "mappings_saved": mappings_saved,
        "offers_saved": offers_saved,
        "original_columns": original_columns,
        "normalized_columns": list(df.columns),
        "normalization_report": normalization_report,
        "quality_report": build_quality_report(
            df=df,
            normalization_report=normalization_report,
        ),
        "filter_suggestions": build_filter_suggestions(df),
        "filter_summary": filter_summary,
        "preview": df.head(50).to_dict(orient="records"),
    }


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

    file_hash = hashlib.sha256(content).hexdigest()
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
    now = datetime.now(timezone.utc)

    supplier.price_etag = metadata.get("etag")
    supplier.price_last_modified = metadata.get("last_modified")
    supplier.price_content_length = (
        metadata.get("content_length")
        or len(content)
    )
    supplier.price_file_hash = file_hash
    supplier.price_data_hash = data_hash
    supplier.price_last_filename = filename
    supplier.price_update_status = "current"
    supplier.price_last_checked_at = now
    supplier.price_last_downloaded_at = now

    if previous_file_hash is None or changed:
        supplier.price_last_changed_at = now

    await session.commit()

    draft = create_import_draft(
        supplier_name=supplier.name,
        supplier_id=supplier.id,
        filename=filename,
        df=df,
        original_columns=original_columns,
        normalization_report=normalization_report,
    )

    result = apply_saved_filter_profile(
        draft=draft,
        filters=supplier.import_filter_profile,
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

    return await commit_import_draft(
        session=session,
        supplier_name=draft["supplier_name"],
        supplier_id=draft.get("supplier_id"),
        filename=draft["filename"],
        df=df,
        original_columns=draft["original_columns"],
        normalization_report=draft["normalization_report"],
        filter_summary=filter_summary,
    )


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
