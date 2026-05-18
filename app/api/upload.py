from fastapi import APIRouter, UploadFile, File, Depends, Query
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
from app.services.supplier_offer_service import save_supplier_offers

router = APIRouter()


@router.post("/upload")
async def upload_csv(
    supplier_name: str = Query(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
):
    df = await parse_file(file)

    original_columns = list(df.columns)

    df, normalization_report = normalize_columns(df)

    df = clean_dataframe(df)

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
        filename=file.filename,
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
        "filename": file.filename,
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