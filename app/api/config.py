from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.config_schemas import (
    PipelineSettingsUpdate,
    ResearchRulesUpdate,
)
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
        "supplier_id": rules.supplier_id,
        "is_supplier_profile": rules.supplier_id is not None,
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
        "referral_fee_percent": float(rules.referral_fee_percent),
        "fulfillment_fee_fixed": float(rules.fulfillment_fee_fixed),
        "max_sales_rank": rules.max_sales_rank,
        "min_monthly_sales": rules.min_monthly_sales,
        "exclude_amazon_in_stock": rules.exclude_amazon_in_stock,
        "lookup_excluded_brands": rules.lookup_excluded_brands or [],
        "lookup_excluded_title_keywords": (
            rules.lookup_excluded_title_keywords or []
        ),
        "lookup_min_cost": (
            float(rules.lookup_min_cost)
            if rules.lookup_min_cost is not None
            else None
        ),
        "lookup_max_cost": (
            float(rules.lookup_max_cost)
            if rules.lookup_max_cost is not None
            else None
        ),

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
    values: PipelineSettingsUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = ConfigService(db)
    settings = await service.update_pipeline_settings(
        values.model_dump(exclude_unset=True)
    )

    return serialize_pipeline_settings(settings)


@router.get("/research-rules")
async def get_research_rules(
    supplier_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    service = ConfigService(db)
    rules = await service.get_research_rules(supplier_id=supplier_id)

    return serialize_research_rules(rules)


@router.post("/research-rules/reset")
async def reset_research_rules(
    supplier_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    service = ConfigService(db)
    rules = await service.reset_research_rules(supplier_id=supplier_id)

    return serialize_research_rules(rules)


@router.patch("/research-rules")
async def update_research_rules(
    values: ResearchRulesUpdate,
    supplier_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    service = ConfigService(db)
    rules = await service.update_research_rules(
        values.model_dump(exclude_unset=True),
        supplier_id=supplier_id,
    )

    return serialize_research_rules(rules)
