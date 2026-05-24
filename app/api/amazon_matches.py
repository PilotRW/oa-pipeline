from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.amazon_match_service import AmazonMatchService

router = APIRouter(
    prefix="/amazon-matches",
    tags=["amazon-matches"],
)


@router.post("/create-pending")
async def create_pending_matches(
    min_priority_score: float | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=1000),
    supplier_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    service = AmazonMatchService(db)

    created_count = await service.create_pending_matches(
        min_priority_score=min_priority_score,
        limit=limit,
        supplier_id=supplier_id,
    )

    return {
        "created_count": created_count,
        "status": "ok",
    }


@router.post("/process-pending")
async def process_pending_matches(
    limit: int | None = Query(default=None, ge=1, le=500),
    supplier_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    service = AmazonMatchService(db)

    result = await service.process_pending_matches(
        limit=limit,
        supplier_id=supplier_id,
    )

    return {
        "status": "ok",
        **result,
    }


@router.get("/")
async def list_amazon_matches(
    match_status: str | None = Query(default=None),
    supplier_id: int | None = Query(default=None, ge=1),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    service = AmazonMatchService(db)

    items = await service.list_matches(
        match_status=match_status,
        supplier_id=supplier_id,
        limit=limit,
        offset=offset,
    )

    return items
