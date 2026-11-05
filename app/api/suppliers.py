from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.amazon_product_match import AmazonProductMatch
from app.models.deal_candidate import DealCandidate
from app.models.ingestion_run import IngestionRun
from app.models.market_snapshot import MarketSnapshot
from app.models.offer_research_queue import OfferResearchQueue
from app.models.supplier import Supplier
from app.models.supplier_offer import SupplierOffer
from app.services.supplier_price_service import (
    SupplierPriceDownloadError,
    check_supplier_price,
    download_supplier_price,
    validate_public_price_url,
)
from app.services.price_file_fingerprint import price_file_fingerprint
from app.services.supplier_import_service import (
    delete_old_supplier_imports,
    delete_supplier_import,
    latest_import_id,
)

router = APIRouter(
    prefix="/suppliers",
    tags=["suppliers"],
)


class SupplierVisibilityPayload(BaseModel):
    is_visible: bool


class SupplierPriceSourcePayload(BaseModel):
    price_url: str | None = None


class SupplierCreatePayload(BaseModel):
    name: str
    price_url: str | None = None


class SupplierPricingPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prices_include_vat: bool
    default_vat_rate: Decimal | None = Field(default=None, ge=0, le=100)


def supplier_price_tracking(supplier: Supplier) -> dict:
    return {
        "price_update_status": (
            supplier.price_update_status
            or ("never_downloaded" if supplier.price_url else "not_configured")
        ),
        "price_last_checked_at": supplier.price_last_checked_at,
        "price_last_downloaded_at": supplier.price_last_downloaded_at,
        "price_last_changed_at": supplier.price_last_changed_at,
        "price_last_filename": supplier.price_last_filename,
        "price_content_length": supplier.price_content_length,
    }


@router.post("/")
async def create_supplier(
    payload: SupplierCreatePayload,
    db: AsyncSession = Depends(get_db),
):
    name = payload.name.strip().lower()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Supplier name is required",
        )

    existing = await db.execute(
        select(Supplier).where(
            func.lower(Supplier.name) == name
        )
    )

    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=409,
            detail="Supplier already exists",
        )

    price_url = str(payload.price_url or "").strip() or None

    if price_url:
        try:
            price_url = validate_public_price_url(price_url)
        except SupplierPriceDownloadError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            ) from exc

    supplier = Supplier(
        name=name,
        price_url=price_url,
        is_visible=True,
    )
    db.add(supplier)
    await db.commit()
    await db.refresh(supplier)

    return {
        "id": supplier.id,
        "name": supplier.name,
        "is_visible": supplier.is_visible,
        "price_url": supplier.price_url,
        "prices_include_vat": supplier.prices_include_vat,
        "default_vat_rate": (
            float(supplier.default_vat_rate)
            if supplier.default_vat_rate is not None
            else None
        ),
        "has_saved_import_filters": False,
        "offers_count": 0,
        **supplier_price_tracking(supplier),
    }


@router.get("/")
async def list_suppliers(
    include_hidden: bool = Query(default=False),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(
            Supplier.id,
            Supplier.name,
            Supplier.is_visible,
            Supplier.price_url,
            Supplier.prices_include_vat,
            Supplier.default_vat_rate,
            Supplier.import_filter_profile,
            Supplier.price_update_status,
            Supplier.price_last_checked_at,
            Supplier.price_last_downloaded_at,
            Supplier.price_last_changed_at,
            Supplier.price_last_filename,
            Supplier.price_content_length,
            func.count(SupplierOffer.id).label("offers_count"),
        )
        .outerjoin(
            SupplierOffer,
            SupplierOffer.supplier_id == Supplier.id,
        )
        .group_by(
            Supplier.id,
            Supplier.name,
            Supplier.is_visible,
            Supplier.price_url,
            Supplier.prices_include_vat,
            Supplier.default_vat_rate,
            Supplier.import_filter_profile,
            Supplier.price_update_status,
            Supplier.price_last_checked_at,
            Supplier.price_last_downloaded_at,
            Supplier.price_last_changed_at,
            Supplier.price_last_filename,
            Supplier.price_content_length,
        )
        .order_by(Supplier.name.asc())
    )

    if not include_hidden:
        query = query.where(Supplier.is_visible.is_(True))

    result = await db.execute(query)
    rows = result.all()

    return [
        {
            "id": supplier_id,
            "name": name,
            "is_visible": is_visible,
            "price_url": price_url,
            "prices_include_vat": prices_include_vat,
            "default_vat_rate": (
                float(default_vat_rate)
                if default_vat_rate is not None
                else None
            ),
            "has_saved_import_filters": bool(import_filter_profile),
            "price_update_status": (
                price_update_status
                or ("never_downloaded" if price_url else "not_configured")
            ),
            "price_last_checked_at": price_last_checked_at,
            "price_last_downloaded_at": price_last_downloaded_at,
            "price_last_changed_at": price_last_changed_at,
            "price_last_filename": price_last_filename,
            "price_content_length": price_content_length,
            "offers_count": offers_count,
        }
        for (
            supplier_id,
            name,
            is_visible,
            price_url,
            prices_include_vat,
            default_vat_rate,
            import_filter_profile,
            price_update_status,
            price_last_checked_at,
            price_last_downloaded_at,
            price_last_changed_at,
            price_last_filename,
            price_content_length,
            offers_count,
        ) in rows
    ]


@router.get("/imports/history")
async def list_supplier_imports(
    limit: int = Query(default=500, ge=1, le=5000),
    db: AsyncSession = Depends(get_db),
):
    rows = (
        await db.execute(
            select(IngestionRun, Supplier)
            .join(Supplier, Supplier.id == IngestionRun.supplier_id)
            .order_by(
                IngestionRun.created_at.desc(),
                IngestionRun.id.desc(),
            )
            .limit(limit)
        )
    ).all()
    active_supplier_ids: set[int] = set()
    result = []

    for run, supplier in rows:
        is_active = supplier.id not in active_supplier_ids
        active_supplier_ids.add(supplier.id)
        result.append({
            "id": run.id,
            "supplier_id": supplier.id,
            "supplier_name": supplier.name,
            "filename": run.filename,
            "status": run.status,
            "rows_total": run.rows_total,
            "rows_valid": run.rows_valid,
            "rows_failed": run.rows_failed,
            "created_at": run.created_at,
            "is_active": is_active,
        })

    return result


@router.delete("/imports/history")
async def delete_expired_import_history(
    older_than_days: int = Query(default=30, ge=1, le=3650),
    db: AsyncSession = Depends(get_db),
):
    cutoff = (
        datetime.now(timezone.utc) - timedelta(days=older_than_days)
    ).replace(tzinfo=None)
    suppliers = (
        await db.execute(
            select(Supplier)
            .join(IngestionRun, IngestionRun.supplier_id == Supplier.id)
            .where(IngestionRun.created_at < cutoff)
            .distinct()
        )
    ).scalars().all()
    totals = {
        "status": "ok",
        "older_than_days": older_than_days,
        "deleted_imports": 0,
        "deleted_rows_reported": 0,
        "current_catalogs_deleted": 0,
        "deleted_catalog": {},
    }

    for supplier in suppliers:
        result = await delete_old_supplier_imports(
            db,
            supplier,
            older_than_days,
        )
        totals["deleted_imports"] += result["deleted_imports"]
        totals["deleted_rows_reported"] += result["deleted_rows_reported"]
        if result["current_catalog_deleted"]:
            totals["current_catalogs_deleted"] += 1
        for key, value in result["deleted_catalog"].items():
            totals["deleted_catalog"][key] = (
                totals["deleted_catalog"].get(key, 0) + value
            )

    return totals


async def count_supplier_statuses(
    db: AsyncSession,
    supplier_id: int,
) -> dict:
    queue_query = (
        select(OfferResearchQueue.status, func.count())
        .where(OfferResearchQueue.supplier_id == supplier_id)
        .group_by(OfferResearchQueue.status)
    )
    matches_query = (
        select(AmazonProductMatch.match_status, func.count())
        .join(
            SupplierOffer,
            SupplierOffer.id == AmazonProductMatch.supplier_offer_id,
        )
        .where(SupplierOffer.supplier_id == supplier_id)
        .group_by(AmazonProductMatch.match_status)
    )
    deals_query = (
        select(DealCandidate.status, func.count())
        .join(
            SupplierOffer,
            SupplierOffer.id == DealCandidate.supplier_offer_id,
        )
        .where(SupplierOffer.supplier_id == supplier_id)
        .group_by(DealCandidate.status)
    )
    snapshots_query = (
        select(MarketSnapshot.snapshot_status, func.count())
        .join(
            SupplierOffer,
            SupplierOffer.id == MarketSnapshot.supplier_offer_id,
        )
        .where(SupplierOffer.supplier_id == supplier_id)
        .group_by(MarketSnapshot.snapshot_status)
    )

    queue_rows = (await db.execute(queue_query)).all()
    match_rows = (await db.execute(matches_query)).all()
    snapshot_rows = (await db.execute(snapshots_query)).all()
    deal_rows = (await db.execute(deals_query)).all()

    return {
        "research_queue": {status: count for status, count in queue_rows},
        "amazon_matches": {status: count for status, count in match_rows},
        "market_snapshots": {
            status: count
            for status, count in snapshot_rows
        },
        "deal_candidates": {status: count for status, count in deal_rows},
    }


@router.get("/dashboard")
async def supplier_dashboard(
    db: AsyncSession = Depends(get_db),
):
    suppliers = await list_suppliers(include_hidden=False, db=db)
    items = []

    for supplier in suppliers:
        runs_query = (
            select(IngestionRun)
            .where(IngestionRun.supplier_id == supplier["id"])
            .order_by(IngestionRun.created_at.desc())
            .limit(5)
        )
        runs = (await db.execute(runs_query)).scalars().all()
        statuses = await count_supplier_statuses(
            db=db,
            supplier_id=supplier["id"],
        )

        items.append(
            {
                **supplier,
                "statuses": statuses,
                "recent_imports": [
                    {
                        "id": run.id,
                        "filename": run.filename,
                        "status": run.status,
                        "rows_total": run.rows_total,
                        "rows_valid": run.rows_valid,
                        "rows_failed": run.rows_failed,
                        "created_at": run.created_at,
                    }
                    for run in runs
                ],
            }
        )

    return items


@router.patch("/{supplier_id}/visibility")
async def update_supplier_visibility(
    supplier_id: int,
    payload: SupplierVisibilityPayload,
    db: AsyncSession = Depends(get_db),
):
    supplier = await db.get(Supplier, supplier_id)

    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    supplier.is_visible = payload.is_visible
    await db.commit()
    await db.refresh(supplier)

    return {
        "id": supplier.id,
        "name": supplier.name,
        "is_visible": supplier.is_visible,
    }


@router.patch("/{supplier_id}/price-source")
async def update_supplier_price_source(
    supplier_id: int,
    payload: SupplierPriceSourcePayload,
    db: AsyncSession = Depends(get_db),
):
    supplier = await db.get(Supplier, supplier_id)

    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    price_url = str(payload.price_url or "").strip()

    if price_url:
        try:
            price_url = validate_public_price_url(price_url)
        except SupplierPriceDownloadError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            ) from exc
    else:
        price_url = None

    if supplier.price_url != price_url:
        supplier.price_etag = None
        supplier.price_last_modified = None
        supplier.price_content_length = None
        supplier.price_file_hash = None
        supplier.price_data_hash = None
        supplier.price_last_filename = None
        supplier.price_update_status = (
            "never_downloaded" if price_url else "not_configured"
        )
        supplier.price_last_checked_at = None
        supplier.price_last_downloaded_at = None
        supplier.price_last_changed_at = None

    supplier.price_url = price_url
    await db.commit()
    await db.refresh(supplier)

    return {
        "id": supplier.id,
        "name": supplier.name,
        "price_url": supplier.price_url,
        "has_saved_import_filters": bool(
            supplier.import_filter_profile
        ),
        **supplier_price_tracking(supplier),
    }


@router.patch("/{supplier_id}/pricing")
async def update_supplier_pricing(
    supplier_id: int,
    payload: SupplierPricingPayload,
    db: AsyncSession = Depends(get_db),
):
    supplier = await db.get(Supplier, supplier_id)

    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    supplier.prices_include_vat = payload.prices_include_vat
    supplier.default_vat_rate = payload.default_vat_rate
    await db.commit()
    await db.refresh(supplier)

    return {
        "id": supplier.id,
        "name": supplier.name,
        "prices_include_vat": supplier.prices_include_vat,
        "default_vat_rate": (
            float(supplier.default_vat_rate)
            if supplier.default_vat_rate is not None
            else None
        ),
    }


@router.post("/{supplier_id}/check-price-update")
async def check_supplier_price_update(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
):
    supplier = await db.get(Supplier, supplier_id)

    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    if not supplier.price_url:
        raise HTTPException(
            status_code=400,
            detail="Supplier price URL is not configured",
        )

    try:
        result = await check_supplier_price(
            supplier.price_url,
            previous_etag=supplier.price_etag,
            previous_last_modified=supplier.price_last_modified,
            previous_content_length=supplier.price_content_length,
            has_downloaded_file=bool(supplier.price_file_hash),
        )

        needs_fingerprint_check = (
            bool(supplier.price_file_hash)
            and result["update_status"] in {
                "no_changes",
                "verification_required",
            }
        )

        if needs_fingerprint_check:
            content, filename, metadata = await download_supplier_price(
                supplier.price_url
            )
            fingerprint = price_file_fingerprint(
                content=content,
                filename=filename,
            )
            file_changed = (
                supplier.price_file_hash != fingerprint["file_hash"]
            )
            data_changed = (
                supplier.price_data_hash != fingerprint["data_hash"]
            )

            result = {
                **result,
                **metadata,
                "update_status": (
                    "new_available"
                    if file_changed or data_changed
                    else "no_changes"
                ),
                "checked_at": result["checked_at"],
                "verified_by_download": True,
                "verified_filename": filename,
                "verified_file_hash": fingerprint["file_hash"],
                "verified_data_hash": fingerprint["data_hash"],
                "verified_row_count": fingerprint["row_count"],
                "file_changed": file_changed,
                "data_changed": data_changed,
            }
    except (SupplierPriceDownloadError, ValueError) as exc:
        supplier.price_update_status = "check_failed"
        await db.commit()
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    supplier.price_update_status = result["update_status"]
    supplier.price_last_checked_at = result["checked_at"]
    await db.commit()
    await db.refresh(supplier)

    return {
        "id": supplier.id,
        "name": supplier.name,
        **result,
        **supplier_price_tracking(supplier),
    }


@router.get("/{supplier_id}")
async def supplier_detail(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
):
    supplier = await db.get(Supplier, supplier_id)

    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    offer_stats_query = select(
        func.count(SupplierOffer.id).label("total"),
        func.count(SupplierOffer.ean)
        .filter(SupplierOffer.ean.isnot(None))
        .label("with_ean"),
        func.count(SupplierOffer.brand)
        .filter(SupplierOffer.brand.isnot(None))
        .label("with_brand"),
        func.count(SupplierOffer.title)
        .filter(SupplierOffer.title.isnot(None))
        .label("with_title"),
        func.count(SupplierOffer.stock)
        .filter(SupplierOffer.stock.isnot(None))
        .label("with_stock"),
        func.avg(SupplierOffer.cost).label("avg_cost"),
    ).where(SupplierOffer.supplier_id == supplier_id)
    offer_stats = (await db.execute(offer_stats_query)).one()

    runs_query = (
        select(IngestionRun)
        .where(IngestionRun.supplier_id == supplier_id)
        .order_by(IngestionRun.created_at.desc())
        .limit(50)
    )
    runs = (await db.execute(runs_query)).scalars().all()
    active_import_id = await latest_import_id(db, supplier_id)

    recent_offers_query = (
        select(SupplierOffer)
        .where(SupplierOffer.supplier_id == supplier_id)
        .order_by(SupplierOffer.imported_at.desc(), SupplierOffer.id.desc())
        .limit(12)
    )
    recent_offers = (await db.execute(recent_offers_query)).scalars().all()
    statuses = await count_supplier_statuses(db=db, supplier_id=supplier_id)

    return {
        "id": supplier.id,
        "name": supplier.name,
        "is_visible": supplier.is_visible,
        "price_url": supplier.price_url,
        "prices_include_vat": supplier.prices_include_vat,
        "default_vat_rate": (
            float(supplier.default_vat_rate)
            if supplier.default_vat_rate is not None
            else None
        ),
        "import_filter_profile": supplier.import_filter_profile,
        "has_saved_import_filters": bool(
            supplier.import_filter_profile
        ),
        "price_etag": supplier.price_etag,
        "price_last_modified": supplier.price_last_modified,
        "price_file_hash": supplier.price_file_hash,
        "price_data_hash": supplier.price_data_hash,
        **supplier_price_tracking(supplier),
        "created_at": supplier.created_at,
        "offer_stats": {
            "total": offer_stats.total,
            "with_ean": offer_stats.with_ean,
            "with_brand": offer_stats.with_brand,
            "with_title": offer_stats.with_title,
            "with_stock": offer_stats.with_stock,
            "avg_cost": (
                float(offer_stats.avg_cost)
                if offer_stats.avg_cost is not None
                else None
            ),
        },
        "statuses": statuses,
        "import_history": [
            {
                "id": run.id,
                "filename": run.filename,
                "files": sorted({
                    item.get("file")
                    for item in (run.normalization_report or [])
                    if item.get("file")
                }) or [run.filename],
                "status": run.status,
                "rows_total": run.rows_total,
                "rows_valid": run.rows_valid,
                "rows_failed": run.rows_failed,
                "mapped_columns": sum(
                    1
                    for item in (run.normalization_report or [])
                    if item.get("mapped_to")
                ),
                "total_columns": len(run.normalization_report or []),
                "created_at": run.created_at,
                "is_active": run.id == active_import_id,
            }
            for run in runs
        ],
        "recent_offers": [
            {
                "id": offer.id,
                "supplier_sku": offer.supplier_sku,
                "ean": offer.ean,
                "brand": offer.brand,
                "title": offer.title,
                "cost": float(offer.cost) if offer.cost is not None else None,
                "vat_rate": (
                    float(offer.vat_rate)
                    if offer.vat_rate is not None
                    else None
                ),
                "currency": offer.currency,
                "stock": offer.stock,
                "source_file": (
                    offer.raw_data.get("source_file")
                    if isinstance(offer.raw_data, dict)
                    else None
                ),
                "imported_at": offer.imported_at,
            }
            for offer in recent_offers
        ],
    }


@router.delete("/{supplier_id}/imports")
async def delete_expired_supplier_imports(
    supplier_id: int,
    older_than_days: int = Query(default=30, ge=1, le=3650),
    db: AsyncSession = Depends(get_db),
):
    supplier = await db.get(Supplier, supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return await delete_old_supplier_imports(
        db,
        supplier,
        older_than_days,
    )


@router.delete("/{supplier_id}/imports/{run_id}")
async def delete_supplier_import_run(
    supplier_id: int,
    run_id: int,
    db: AsyncSession = Depends(get_db),
):
    supplier = await db.get(Supplier, supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    run = await db.get(IngestionRun, run_id)
    if run is None or run.supplier_id != supplier_id:
        raise HTTPException(status_code=404, detail="Import not found")

    return await delete_supplier_import(db, supplier, run)
