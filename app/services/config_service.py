from decimal import Decimal

from sqlalchemy import delete, select
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

    research_rule_fields = {
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
        "lookup_excluded_brands",
        "lookup_excluded_title_keywords",
        "lookup_min_cost",
        "lookup_max_cost",
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
    system_research_rule_defaults = {
        "min_priority_score": Decimal("80"),
        "min_stock": 1,
        "low_stock_threshold": 1,
        "medium_stock_threshold": 3,
        "high_stock_threshold": 20,
        "preferred_cost_min": Decimal("20"),
        "preferred_cost_max": Decimal("300"),
        "medium_cost_max": Decimal("1000"),
        "min_cost": Decimal("5"),
        "min_roi_percent": Decimal("20"),
        "min_profit": Decimal("0"),
        "referral_fee_percent": Decimal("15"),
        "fulfillment_fee_fixed": Decimal("5"),
        "max_sales_rank": None,
        "min_monthly_sales": None,
        "exclude_amazon_in_stock": False,
        "lookup_excluded_brands": [],
        "lookup_excluded_title_keywords": [],
        "lookup_min_cost": None,
        "lookup_max_cost": None,
        "score_stock_high": 30,
        "score_stock_medium": 20,
        "score_stock_low": 10,
        "score_stock_very_low": -20,
        "score_cost_preferred": 30,
        "score_cost_medium": 15,
        "score_cost_high": -10,
        "score_cost_low": -20,
        "score_brand_present": 15,
        "score_title_present": 15,
        "score_ean_present": 10,
    }

    async def get_research_rules(
        self,
        supplier_id: int | None = None,
    ) -> ResearchRule:
        if supplier_id is not None:
            supplier_result = await self.db.execute(
                select(ResearchRule).where(
                    ResearchRule.supplier_id == supplier_id
                )
            )
            supplier_rules = supplier_result.scalar_one_or_none()

            if supplier_rules is not None:
                return supplier_rules

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
        supplier_id: int | None = None,
    ) -> ResearchRule:
        rules = await self.get_research_rules(supplier_id=supplier_id)

        if supplier_id is not None and rules.supplier_id != supplier_id:
            global_rules = rules
            rules = ResearchRule(
                supplier_id=supplier_id,
                **{
                    field: getattr(global_rules, field)
                    for field in self.research_rule_fields
                },
            )
            self.db.add(rules)

        for key, value in values.items():
            if key in self.research_rule_fields:
                setattr(rules, key, value)

        await self.db.commit()
        await self.db.refresh(rules)

        return rules

    async def reset_research_rules(
        self,
        supplier_id: int | None = None,
    ) -> ResearchRule:
        if supplier_id is not None:
            await self.db.execute(
                delete(ResearchRule).where(
                    ResearchRule.supplier_id == supplier_id
                )
            )
            await self.db.commit()

            return await self.get_research_rules(supplier_id=supplier_id)

        rules = await self.get_research_rules()

        for key, value in self.system_research_rule_defaults.items():
            setattr(rules, key, value)

        await self.db.commit()
        await self.db.refresh(rules)

        return rules
