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
from app.ingestion.cleaners import tester_mask


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
    source_files: list[str] | None = None,
    skipped_files: list[str] | None = None,
    file_diagnostics: list[dict] | None = None,
    supply_channel_assignments: dict[str, str] | None = None,
    supply_channel_suggestions: list[dict] | None = None,
) -> dict:
    settings = await ConfigService(session).get_pipeline_settings()
    df = df.loc[~tester_mask(df)].copy()
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

    assignments = supply_channel_assignments or {filename: "stock"}
    suggestions = {
        item.get("filename"): item
        for item in (supply_channel_suggestions or [])
    }
    df = df.copy()
    if "source_file" in df.columns:
        source_names = df["source_file"].astype(str)
    else:
        source_names = [filename] * len(df)
    df["supply_channel"] = [
        assignments.get(source_name, "stock")
        for source_name in source_names
    ]

    def lead_time(source_name, field):
        suggestion = suggestions.get(source_name, {})
        selected = assignments.get(source_name, "stock")
        if selected == "stock":
            return 0
        if selected != suggestion.get("channel"):
            return None
        return suggestion.get(field)

    df["lead_time_min_days"] = [
        lead_time(source_name, "lead_time_min_days")
        for source_name in source_names
    ]
    df["lead_time_max_days"] = [
        lead_time(source_name, "lead_time_max_days")
        for source_name in source_names
    ]

    rows_total = len(df)
    ingestion_run = await save_ingestion_run(
        session=session,
        supplier_id=supplier.id,
        filename=filename,
        rows_total=rows_total,
        rows_valid=rows_total,
        rows_failed=0,
        normalization_report=normalization_report,
        supply_channel_assignments=assignments,
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
        "filenames": source_files or [filename],
        "file_count": len(source_files or [filename]),
        "skipped_files": skipped_files or [],
        "skipped_file_count": len(skipped_files or []),
        "file_diagnostics": file_diagnostics or [],
        "supply_channel_assignments": assignments,
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
