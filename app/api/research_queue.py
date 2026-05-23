from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.research_queue_service import ResearchQueueService

router = APIRouter(
    prefix="/research-queue",
    tags=["research-queue"],
)


@router.post("/populate")
async def populate_research_queue(
    db: AsyncSession = Depends(get_db),
):
    service = ResearchQueueService(db)

    created_count = await service.populate_queue_from_supplier_offers()

    return {
        "created_count": created_count,
        "status": "ok",
    }


@router.post("/recalculate-priority")
async def recalculate_priority(
    db: AsyncSession = Depends(get_db),
):
    service = ResearchQueueService(db)

    updated_count = await service.recalculate_priority_scores()

    return {
        "updated_count": updated_count,
        "status": "ok",
    }


@router.get("/")
async def list_research_queue(
    status: str | None = Query(default=None),
    min_priority_score: float | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    service = ResearchQueueService(db)

    items = await service.list_queue(
        status=status,
        min_priority_score=min_priority_score,
        limit=limit,
        offset=offset,
    )

    return items