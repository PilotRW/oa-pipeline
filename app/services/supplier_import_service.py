from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ingestion_run import IngestionRun
from app.models.supplier import Supplier
from app.services.supplier_offer_service import delete_supplier_catalog_data


def reset_supplier_price_tracking(supplier: Supplier) -> None:
    supplier.price_etag = None
    supplier.price_last_modified = None
    supplier.price_content_length = None
    supplier.price_file_hash = None
    supplier.price_data_hash = None
    supplier.price_last_filename = None
    supplier.price_update_status = (
        "never_downloaded" if supplier.price_url else "not_configured"
    )
    supplier.price_last_checked_at = None
    supplier.price_last_downloaded_at = None
    supplier.price_last_changed_at = None


async def latest_import_id(
    db: AsyncSession,
    supplier_id: int,
) -> int | None:
    result = await db.execute(
        select(IngestionRun.id)
        .where(IngestionRun.supplier_id == supplier_id)
        .order_by(IngestionRun.created_at.desc(), IngestionRun.id.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def delete_supplier_import(
    db: AsyncSession,
    supplier: Supplier,
    run: IngestionRun,
) -> dict:
    active_import_id = await latest_import_id(db, supplier.id)
    deletes_current_catalog = run.id == active_import_id
    deleted_catalog = {}

    if deletes_current_catalog:
        deleted_catalog = await delete_supplier_catalog_data(
            db,
            supplier.id,
        )
        reset_supplier_price_tracking(supplier)

    await db.delete(run)
    await db.commit()

    return {
        "status": "ok",
        "supplier_id": supplier.id,
        "deleted_imports": 1,
        "deleted_rows_reported": int(run.rows_total or 0),
        "current_catalog_deleted": deletes_current_catalog,
        "deleted_catalog": deleted_catalog,
    }


async def delete_old_supplier_imports(
    db: AsyncSession,
    supplier: Supplier,
    older_than_days: int,
) -> dict:
    cutoff = (
        datetime.now(timezone.utc) - timedelta(days=older_than_days)
    ).replace(tzinfo=None)
    runs = (
        await db.execute(
            select(IngestionRun).where(
                IngestionRun.supplier_id == supplier.id,
                IngestionRun.created_at < cutoff,
            )
        )
    ).scalars().all()

    if not runs:
        return {
            "status": "ok",
            "supplier_id": supplier.id,
            "older_than_days": older_than_days,
            "deleted_imports": 0,
            "deleted_rows_reported": 0,
            "current_catalog_deleted": False,
            "deleted_catalog": {},
        }

    run_ids = [run.id for run in runs]
    active_import_id = await latest_import_id(db, supplier.id)
    deletes_current_catalog = active_import_id in run_ids
    deleted_catalog = {}

    if deletes_current_catalog:
        deleted_catalog = await delete_supplier_catalog_data(
            db,
            supplier.id,
        )
        reset_supplier_price_tracking(supplier)

    await db.execute(
        delete(IngestionRun).where(IngestionRun.id.in_(run_ids))
    )
    await db.commit()

    return {
        "status": "ok",
        "supplier_id": supplier.id,
        "older_than_days": older_than_days,
        "deleted_imports": len(runs),
        "deleted_rows_reported": sum(
            int(run.rows_total or 0)
            for run in runs
        ),
        "current_catalog_deleted": deletes_current_catalog,
        "deleted_catalog": deleted_catalog,
    }
