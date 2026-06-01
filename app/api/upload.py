from pydantic import BaseModel

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.ingestion.parser import parse_file
from app.ingestion.normalizer import normalize_columns
from app.ingestion.cleaners import clean_dataframe
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


async def commit_import_draft(
    *,
    session: AsyncSession,
    supplier_name: str,
    filename: str,
    df,
    original_columns: list,
    normalization_report: list[dict],
    filter_summary: dict | None = None,
):
    settings = await ConfigService(
        session
    ).get_pipeline_settings()

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
):
    df, original_columns, normalization_report = await build_import_dataframe(file)

    draft = create_import_draft(
        supplier_name=supplier_name,
        filename=file.filename,
        df=df,
        original_columns=original_columns,
        normalization_report=normalization_report,
    )

    return serialize_import_draft(draft)


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
        filename=draft["filename"],
        df=df,
        original_columns=draft["original_columns"],
        normalization_report=draft["normalization_report"],
        filter_summary=filter_summary,
    )


@router.post("/upload/filter-preview")
async def preview_import_filters(
    payload: ImportFilterPreviewRequest,
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
    draft["confirmed_filters"] = payload.filters
    draft["filter_summary"] = filter_summary

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
        content=df.to_csv(index=False).encode("utf-8-sig"),
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
        filename=file.filename,
        df=df,
        original_columns=original_columns,
        normalization_report=normalization_report,
    )
