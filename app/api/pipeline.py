from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.amazon_product_match import AmazonProductMatch
from app.models.deal_candidate import DealCandidate
from app.models.keepa_product_metric import KeepaProductMetric
from app.models.offer_research_queue import OfferResearchQueue
from app.services.amazon_match_service import AmazonMatchService
from app.services.deal_service import DealService
from app.services.keepa_service import KeepaService

router = APIRouter(
    prefix="/pipeline",
    tags=["pipeline"],
)


@router.post("/run-batch")
async def run_pipeline_batch(
    min_priority_score: float = Query(default=80),
    limit: int = Query(default=20, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    amazon_service = AmazonMatchService(db)
    keepa_service = KeepaService(db)
    deal_service = DealService(db)

    amazon_pending_created = await amazon_service.create_pending_matches(
        min_priority_score=min_priority_score,
        limit=limit,
    )

    amazon_processed = await amazon_service.process_pending_matches(
        limit=limit,
    )

    keepa_pending_created = await keepa_service.create_pending_metrics(
        limit=limit,
    )

    keepa_processed = await keepa_service.process_pending_metrics(
        limit=limit,
    )

    deal_candidates_created = await deal_service.create_deal_candidates(
        limit=limit,
    )

    return {
        "status": "ok",
        "amazon_pending_created": amazon_pending_created,
        "amazon_processed": amazon_processed,
        "keepa_pending_created": keepa_pending_created,
        "keepa_processed": keepa_processed,
        "deal_candidates_created": deal_candidates_created,
    }


async def count_by_status(
    db: AsyncSession,
    model,
    status_column,
) -> dict:
    query = (
        select(
            status_column,
            func.count().label("count"),
        )
        .select_from(model)
        .group_by(status_column)
    )

    result = await db.execute(query)
    rows = result.all()

    return {
        row[0]: row[1]
        for row in rows
    }


@router.get("/summary")
async def pipeline_summary(
    db: AsyncSession = Depends(get_db),
):
    research_queue = await count_by_status(
        db=db,
        model=OfferResearchQueue,
        status_column=OfferResearchQueue.status,
    )

    amazon_matches = await count_by_status(
        db=db,
        model=AmazonProductMatch,
        status_column=AmazonProductMatch.match_status,
    )

    keepa_metrics = await count_by_status(
        db=db,
        model=KeepaProductMetric,
        status_column=KeepaProductMetric.data_status,
    )

    deal_candidates = await count_by_status(
        db=db,
        model=DealCandidate,
        status_column=DealCandidate.status,
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