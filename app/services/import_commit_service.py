from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.supplier import Supplier
from app.services.config_service import ConfigService
from app.services.import_draft_service import (
    build_filter_suggestions,
    build_quality_report,
)
from app.services.ingestion_service import (
    get_or_create_supplier,
    save_column_mappings,
    save_ingestion_run,
)
from app.services.marketplace import currency_for_marketplace
from app.services.supplier_offer_service import save_supplier_offers


class ImportSupplierNotFoundError(LookupError):
    pass


def apply_price_tracking(
    supplier: Supplier,
    price_tracking: dict,
    filename: str,
) -> None:
    now = datetime.now(timezone.utc)
    supplier.price_etag = price_tracking.get("etag")
    supplier.price_last_modified = price_tracking.get("last_modified")
    supplier.price_content_length = price_tracking.get("content_length")
    supplier.price_file_hash = price_tracking.get("file_hash")
    supplier.price_data_hash = price_tracking.get("data_hash")
    supplier.price_last_filename = price_tracking.get("filename") or filename
    supplier.price_update_status = "current"
    supplier.price_last_checked_at = now
    supplier.price_last_downloaded_at = now
    if price_tracking.get("changed"):
        supplier.price_last_changed_at = now


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
    price_tracking: dict | None = None,
) -> dict:
    settings = await ConfigService(session).get_pipeline_settings()
    supplier = (
        await session.get(Supplier, supplier_id)
        if supplier_id is not None
        else None
    )

    if supplier_id is not None and supplier is None:
        raise ImportSupplierNotFoundError(
            "Configured supplier no longer exists"
        )
    if supplier is None:
        supplier = await get_or_create_supplier(
            session=session,
            supplier_name=supplier_name,
        )

    rows_total = len(df)
    ingestion_run = await save_ingestion_run(
        session=session,
        supplier_id=supplier.id,
        filename=filename,
        rows_total=rows_total,
        rows_valid=rows_total,
        rows_failed=0,
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

    if price_tracking:
        apply_price_tracking(supplier, price_tracking, filename)

    await session.commit()
    return {
        "supplier": {"id": supplier.id, "name": supplier.name},
        "ingestion_run": {
            "id": ingestion_run.id,
            "status": ingestion_run.status,
        },
        "filename": filename,
        "rows": rows_total,
        "rows_valid": rows_total,
        "rows_failed": 0,
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
