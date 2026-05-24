from fastapi import APIRouter, Depends
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


@router.get("/")
async def list_suppliers(
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(
            Supplier.id,
            Supplier.name,
            func.count(SupplierOffer.id).label("offers_count"),
        )
        .outerjoin(
            SupplierOffer,
            SupplierOffer.supplier_id == Supplier.id,
        )
        .group_by(Supplier.id, Supplier.name)
        .order_by(Supplier.name.asc())
    )

    result = await db.execute(query)
    rows = result.all()

    return [
        {
            "id": supplier_id,
            "name": name,
            "offers_count": offers_count,
        }
        for supplier_id, name, offers_count in rows
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
    suppliers = await list_suppliers(db=db)
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
