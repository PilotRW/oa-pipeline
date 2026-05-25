from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.amazon_product_match import AmazonProductMatch
from app.models.deal_candidate import DealCandidate
from app.models.ingestion_run import IngestionRun
from app.models.offer_research_queue import OfferResearchQueue
from app.models.supplier import Supplier
from app.models.supplier_offer import SupplierOffer

router = APIRouter(
    prefix="/suppliers",
    tags=["suppliers"],
)


class SupplierVisibilityPayload(BaseModel):
    is_visible: bool


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
            func.count(SupplierOffer.id).label("offers_count"),
        )
        .outerjoin(
            SupplierOffer,
            SupplierOffer.supplier_id == Supplier.id,
        )
        .group_by(Supplier.id, Supplier.name, Supplier.is_visible)
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
            "offers_count": offers_count,
        }
        for supplier_id, name, is_visible, offers_count in rows
    ]


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

    queue_rows = (await db.execute(queue_query)).all()
    match_rows = (await db.execute(matches_query)).all()
    deal_rows = (await db.execute(deals_query)).all()

    return {
        "research_queue": {status: count for status, count in queue_rows},
        "amazon_matches": {status: count for status, count in match_rows},
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
                "currency": offer.currency,
                "stock": offer.stock,
                "imported_at": offer.imported_at,
            }
            for offer in recent_offers
        ],
    }
