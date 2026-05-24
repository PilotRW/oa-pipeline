from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.amazon_product_match import AmazonProductMatch
from app.models.deal_candidate import DealCandidate
from app.models.keepa_product_metric import KeepaProductMetric
from app.models.offer_research_queue import OfferResearchQueue
from app.models.supplier_offer import SupplierOffer
from app.services.pipeline_service import PipelineService

router = APIRouter(
    prefix="/pipeline",
    tags=["pipeline"],
)


@router.post("/run-batch")
async def run_pipeline_batch(
    min_priority_score: float | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=500),
    supplier_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    service = PipelineService(db)

    return await service.run_batch(
        min_priority_score=min_priority_score,
        limit=limit,
        supplier_id=supplier_id,
    )


@router.post("/run-research")
async def run_research(
    min_priority_score: float | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=500),
    supplier_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    service = PipelineService(db)

    return await service.run_research(
        min_priority_score=min_priority_score,
        limit=limit,
        supplier_id=supplier_id,
    )


async def count_by_status(
    db: AsyncSession,
    model,
    status_column,
    supplier_id: int | None = None,
) -> dict:
    query = (
        select(
            status_column,
            func.count().label("count"),
        )
        .select_from(model)
        .group_by(status_column)
    )

    if supplier_id is not None:
        if model is OfferResearchQueue:
            query = query.where(
                OfferResearchQueue.supplier_id == supplier_id
            )
        elif model is AmazonProductMatch:
            query = (
                query
                .join(
                    SupplierOffer,
                    SupplierOffer.id == AmazonProductMatch.supplier_offer_id,
                )
                .where(SupplierOffer.supplier_id == supplier_id)
            )
        elif model is DealCandidate:
            query = (
                query
                .join(
                    SupplierOffer,
                    SupplierOffer.id == DealCandidate.supplier_offer_id,
                )
                .where(SupplierOffer.supplier_id == supplier_id)
            )

    result = await db.execute(query)
    rows = result.all()

    return {
        row[0]: row[1]
        for row in rows
    }


async def count_keepa_by_status(
    db: AsyncSession,
    supplier_id: int | None = None,
) -> dict:
    query = (
        select(
            KeepaProductMetric.data_status,
            func.count().label("count"),
        )
        .select_from(KeepaProductMetric)
    )

    if supplier_id is not None:
        query = (
            query
            .join(
                AmazonProductMatch,
                AmazonProductMatch.asin == KeepaProductMetric.asin,
            )
            .join(
                SupplierOffer,
                SupplierOffer.id == AmazonProductMatch.supplier_offer_id,
            )
            .where(SupplierOffer.supplier_id == supplier_id)
        )

    query = query.group_by(KeepaProductMetric.data_status)

    result = await db.execute(query)
    rows = result.all()

    return {
        row[0]: row[1]
        for row in rows
    }


@router.get("/summary")
async def pipeline_summary(
    supplier_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    research_queue = await count_by_status(
        db=db,
        model=OfferResearchQueue,
        status_column=OfferResearchQueue.status,
        supplier_id=supplier_id,
    )

    amazon_matches = await count_by_status(
        db=db,
        model=AmazonProductMatch,
        status_column=AmazonProductMatch.match_status,
        supplier_id=supplier_id,
    )

    keepa_metrics = await count_keepa_by_status(
        db=db,
        supplier_id=supplier_id,
    )

    deal_candidates = await count_by_status(
        db=db,
        model=DealCandidate,
        status_column=DealCandidate.status,
        supplier_id=supplier_id,
    )

    return {
        "research_queue": {
            "total": sum(research_queue.values()),
            "by_status": research_queue,
        },
        "amazon_matches": {
            "total": sum(amazon_matches.values()),
            "by_status": amazon_matches,
        },
        "keepa_metrics": {
            "total": sum(keepa_metrics.values()),
            "by_status": keepa_metrics,
        },
        "deal_candidates": {
            "total": sum(deal_candidates.values()),
            "by_status": deal_candidates,
        },
    }
