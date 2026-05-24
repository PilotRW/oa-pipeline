from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.config_service import ConfigService

router = APIRouter(
    prefix="/config",
    tags=["config"],
)


def serialize_pipeline_settings(settings):
    return {
        "id": settings.id,
        "use_real_keepa": settings.use_real_keepa,
        "default_batch_size": settings.default_batch_size,
        "default_marketplace": settings.default_marketplace,
        "created_at": settings.created_at,
        "updated_at": settings.updated_at,
    }


def serialize_research_rules(rules):
    return {
        "id": rules.id,
        "min_priority_score": float(rules.min_priority_score),
        "min_stock": rules.min_stock,
        "low_stock_threshold": rules.low_stock_threshold,
        "medium_stock_threshold": rules.medium_stock_threshold,
        "high_stock_threshold": rules.high_stock_threshold,
        "preferred_cost_min": float(rules.preferred_cost_min),
        "preferred_cost_max": float(rules.preferred_cost_max),
        "medium_cost_max": float(rules.medium_cost_max),
        "min_cost": float(rules.min_cost),
        "min_roi_percent": float(rules.min_roi_percent),
        "min_profit": float(rules.min_profit),
        "max_sales_rank": rules.max_sales_rank,
        "min_monthly_sales": rules.min_monthly_sales,
        "exclude_amazon_in_stock": rules.exclude_amazon_in_stock,

        "score_stock_high": rules.score_stock_high,
        "score_stock_medium": rules.score_stock_medium,
        "score_stock_low": rules.score_stock_low,
        "score_stock_very_low": rules.score_stock_very_low,

        "score_cost_preferred": rules.score_cost_preferred,
        "score_cost_medium": rules.score_cost_medium,
        "score_cost_high": rules.score_cost_high,
        "score_cost_low": rules.score_cost_low,

        "score_brand_present": rules.score_brand_present,
        "score_title_present": rules.score_title_present,
        "score_ean_present": rules.score_ean_present,

        "created_at": rules.created_at,
        "updated_at": rules.updated_at,
    }


@router.get("/pipeline-settings")
async def get_pipeline_settings(
    db: AsyncSession = Depends(get_db),
):
    service = ConfigService(db)
    settings = await service.get_pipeline_settings()

    return serialize_pipeline_settings(settings)


@router.patch("/pipeline-settings")
async def update_pipeline_settings(
    values: dict,
    db: AsyncSession = Depends(get_db),
):
    service = ConfigService(db)
    settings = await service.update_pipeline_settings(values)

    return serialize_pipeline_settings(settings)


@router.get("/research-rules")
async def get_research_rules(
    db: AsyncSession = Depends(get_db),
):
    service = ConfigService(db)
    rules = await service.get_research_rules()

    return serialize_research_rules(rules)


@router.patch("/research-rules")
async def update_research_rules(
    values: dict,
    db: AsyncSession = Depends(get_db),
):
    service = ConfigService(db)
    rules = await service.update_research_rules(values)

    return serialize_research_rules(rules)