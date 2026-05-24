from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.keepa_service import KeepaService

router = APIRouter(
    prefix="/keepa",
    tags=["keepa"],
)


@router.post("/create-pending")
async def create_pending_keepa_metrics(
    limit: int | None = Query(default=None, ge=1, le=1000),
    supplier_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    service = KeepaService(db)

    created_count = await service.create_pending_metrics(
        limit=limit,
        supplier_id=supplier_id,
    )

    return {
        "created_count": created_count,
        "status": "ok",
    }


@router.post("/process-pending")
async def process_pending_keepa_metrics(
    limit: int | None = Query(default=None, ge=1, le=500),
    supplier_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    service = KeepaService(db)

    result = await service.process_pending_metrics(
        limit=limit,
        supplier_id=supplier_id,
    )

    return {
        "status": "ok",
        **result,
    }


@router.get("/")
async def list_keepa_metrics(
    data_status: str | None = Query(default=None),
    supplier_id: int | None = Query(default=None, ge=1),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    service = KeepaService(db)

    items = await service.list_metrics(
        data_status=data_status,
        supplier_id=supplier_id,
        limit=limit,
        offset=offset,
    )

    return items
