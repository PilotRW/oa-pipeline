from pydantic import BaseModel

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
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
    consume_import_draft,
    create_import_draft,
    serialize_import_draft,
)
from app.services.marketplace import currency_for_marketplace
from app.services.supplier_offer_service import save_supplier_offers

router = APIRouter()


class ImportCommitRequest(BaseModel):
    import_token: str


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
        "preview": df.head(3).to_dict(orient="records"),
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

    return await commit_import_draft(
        session=session,
        supplier_name=draft["supplier_name"],
        filename=draft["filename"],
        df=draft["df"],
        original_columns=draft["original_columns"],
        normalization_report=draft["normalization_report"],
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
