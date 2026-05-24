from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pipeline_setting import PipelineSetting
from app.models.research_rule import ResearchRule


class ConfigService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_pipeline_settings(self) -> PipelineSetting:
        result = await self.db.execute(
            select(PipelineSetting).where(
                PipelineSetting.id == 1
            )
        )

        settings = result.scalar_one_or_none()

        if settings is None:
            settings = PipelineSetting(
                id=1,
                use_real_keepa=False,
                default_batch_size=20,
                default_marketplace="DE",
            )

            self.db.add(settings)
            await self.db.commit()
            await self.db.refresh(settings)

        return settings

    async def get_research_rules(self) -> ResearchRule:
        result = await self.db.execute(
            select(ResearchRule).where(
                ResearchRule.id == 1
            )
        )

        rules = result.scalar_one_or_none()

        if rules is None:
            rules = ResearchRule(
                id=1,
            )

            self.db.add(rules)
            await self.db.commit()
            await self.db.refresh(rules)

        return rules

    async def update_pipeline_settings(
        self,
        values: dict,
    ) -> PipelineSetting:
        settings = await self.get_pipeline_settings()

        allowed_fields = {
            "use_real_keepa",
            "default_batch_size",
            "default_marketplace",
        }

        for key, value in values.items():
            if key in allowed_fields:
                setattr(settings, key, value)

        await self.db.commit()
        await self.db.refresh(settings)

        return settings

    async def update_research_rules(
        self,
        values: dict,
    ) -> ResearchRule:
        rules = await self.get_research_rules()

        allowed_fields = {
            "min_priority_score",
            "min_stock",
            "low_stock_threshold",
            "medium_stock_threshold",
            "high_stock_threshold",
            "preferred_cost_min",
            "preferred_cost_max",
            "medium_cost_max",
            "min_cost",
            "min_roi_percent",
            "min_profit",
            "referral_fee_percent",
            "fulfillment_fee_fixed",
            "max_sales_rank",
            "min_monthly_sales",
            "exclude_amazon_in_stock",

            # scoring weights
            "score_stock_high",
            "score_stock_medium",
            "score_stock_low",
            "score_stock_very_low",

            "score_cost_preferred",
            "score_cost_medium",
            "score_cost_high",
            "score_cost_low",

            "score_brand_present",
            "score_title_present",
            "score_ean_present",
        }

        for key, value in values.items():
            if key in allowed_fields:
                setattr(rules, key, value)

        await self.db.commit()
        await self.db.refresh(rules)

        return rules
