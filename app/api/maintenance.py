from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.maintenance_service import MaintenanceService

router = APIRouter(
    prefix="/maintenance",
    tags=["maintenance"],
)


class CleanupConfirmation(BaseModel):
    confirmation: str


@router.get("/status")
async def maintenance_status(
    db: AsyncSession = Depends(get_db),
):
    return await MaintenanceService(db).get_status()


@router.post("/clear-workspace")
async def clear_workspace(
    payload: CleanupConfirmation,
    db: AsyncSession = Depends(get_db),
):
    if payload.confirmation != "CLEAR WORKSPACE":
        raise HTTPException(
            status_code=400,
            detail="Confirmation must be CLEAR WORKSPACE",
        )

    return MaintenanceService(db).clear_workspace()


@router.post("/clear-database")
async def clear_database(
    payload: CleanupConfirmation,
    db: AsyncSession = Depends(get_db),
):
    if payload.confirmation != "CLEAR DATABASE":
        raise HTTPException(
            status_code=400,
            detail="Confirmation must be CLEAR DATABASE",
        )

    return await MaintenanceService(
        db
    ).clear_database_data()
