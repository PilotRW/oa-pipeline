from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.deal_service import DealService

router = APIRouter(
    prefix="/deals",
    tags=["deals"],
)


@router.post("/create-candidates")
async def create_deal_candidates(
    limit: int | None = Query(default=None, ge=1, le=1000),
    supplier_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    service = DealService(db)

    created_count = await service.create_deal_candidates(
        limit=limit,
        supplier_id=supplier_id,
    )

    return {
        "created_count": created_count,
        "status": "ok",
    }


@router.get("/")
async def list_deal_candidates(
    status: str | None = Query(default=None),
    min_roi_percent: float | None = Query(default=None),
    supplier_id: int | None = Query(default=None, ge=1),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    service = DealService(db)

    items = await service.list_deal_candidates(
        status=status,
        min_roi_percent=min_roi_percent,
        supplier_id=supplier_id,
        limit=limit,
        offset=offset,
    )

    return items
