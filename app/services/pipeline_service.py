from sqlalchemy.ext.asyncio import AsyncSession

from app.services.amazon_match_service import AmazonMatchService
from app.services.config_service import ConfigService
from app.services.deal_service import DealService
from app.services.keepa_service import KeepaService
from app.services.research_queue_service import ResearchQueueService


class PipelineService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.config_service = ConfigService(db)

    async def run_batch(
        self,
        min_priority_score: float | None = None,
        limit: int | None = None,
        supplier_id: int | None = None,
    ) -> dict:
        settings = await self.config_service.get_pipeline_settings()
        rules = await self.config_service.get_research_rules(
            supplier_id=supplier_id
        )

        batch_limit = (
            limit
            if limit is not None
            else settings.default_batch_size
        )

        priority_score = (
            min_priority_score
            if min_priority_score is not None
            else float(rules.min_priority_score)
        )

        amazon_service = AmazonMatchService(self.db)
        keepa_service = KeepaService(self.db)
        deal_service = DealService(self.db)

        amazon_pending_created = await amazon_service.create_pending_matches(
            min_priority_score=priority_score,
            limit=batch_limit,
            supplier_id=supplier_id,
        )

        amazon_processed = await amazon_service.process_pending_matches(
            limit=batch_limit,
            use_real_keepa=settings.use_real_keepa,
            marketplace=settings.default_marketplace,
            supplier_id=supplier_id,
        )

        keepa_pending_created = await keepa_service.create_pending_metrics(
            limit=batch_limit,
            supplier_id=supplier_id,
        )

        keepa_processed = await keepa_service.process_pending_metrics(
            limit=batch_limit,
            use_real_keepa=settings.use_real_keepa,
            marketplace=settings.default_marketplace,
            supplier_id=supplier_id,
        )

        deal_candidates_created = await deal_service.create_deal_candidates(
            limit=batch_limit,
            supplier_id=supplier_id,
        )

        return {
            "status": "ok",
            "settings": {
                "limit": batch_limit,
                "min_priority_score": priority_score,
                "use_real_keepa": settings.use_real_keepa,
                "marketplace": settings.default_marketplace,
                "supplier_id": supplier_id,
            },
            "amazon_pending_created": amazon_pending_created,
            "amazon_processed": amazon_processed,
            "keepa_pending_created": keepa_pending_created,
            "keepa_processed": keepa_processed,
            "deal_candidates_created": deal_candidates_created,
        }

    async def run_research(
        self,
        min_priority_score: float | None = None,
        limit: int | None = None,
        supplier_id: int | None = None,
        exclude_brands: list[str] | None = None,
        exclude_title_keywords: list[str] | None = None,
        min_cost: float | None = None,
        max_cost: float | None = None,
    ) -> dict:
        settings = await self.config_service.get_pipeline_settings()
        rules = await self.config_service.get_research_rules(
            supplier_id=supplier_id
        )

        batch_limit = (
            limit
            if limit is not None
            else settings.default_batch_size
        )

        priority_score = (
            min_priority_score
            if min_priority_score is not None
            else float(rules.min_priority_score)
        )

        queue_service = ResearchQueueService(self.db)
        amazon_service = AmazonMatchService(self.db)
        effective_exclude_brands = (
            exclude_brands
            if exclude_brands is not None
            else rules.lookup_excluded_brands
        )
        effective_exclude_keywords = (
            exclude_title_keywords
            if exclude_title_keywords is not None
            else rules.lookup_excluded_title_keywords
        )
        effective_min_cost = (
            min_cost
            if min_cost is not None
            else (
                float(rules.lookup_min_cost)
                if rules.lookup_min_cost is not None
                else None
            )
        )
        effective_max_cost = (
            max_cost
            if max_cost is not None
            else (
                float(rules.lookup_max_cost)
                if rules.lookup_max_cost is not None
                else None
            )
        )

        queue_created = await queue_service.populate_queue_from_supplier_offers(
            supplier_id=supplier_id,
        )

        amazon_pending_created = await amazon_service.create_pending_matches(
            min_priority_score=priority_score,
            limit=batch_limit,
            supplier_id=supplier_id,
            exclude_brands=effective_exclude_brands,
            exclude_title_keywords=effective_exclude_keywords,
            min_cost=effective_min_cost,
            max_cost=effective_max_cost,
        )

        amazon_processed = await amazon_service.process_pending_matches(
            limit=batch_limit,
            use_real_keepa=settings.use_real_keepa,
            marketplace=settings.default_marketplace,
            supplier_id=supplier_id,
        )

        return {
            "status": "ok",
            "settings": {
                "limit": batch_limit,
                "min_priority_score": priority_score,
                "use_real_keepa": settings.use_real_keepa,
                "marketplace": settings.default_marketplace,
                "supplier_id": supplier_id,
                "external_filters": {
                    "exclude_brands": amazon_service.normalize_filter_terms(
                        effective_exclude_brands
                    ),
                    "exclude_title_keywords": amazon_service.normalize_filter_terms(
                        effective_exclude_keywords
                    ),
                    "min_cost": effective_min_cost,
                    "max_cost": effective_max_cost,
                },
            },
            "queue_created": queue_created,
            "amazon_pending_created": amazon_pending_created,
            "amazon_processed": amazon_processed,
        }

    async def preview_external_lookup(
        self,
        min_priority_score: float | None = None,
        limit: int | None = None,
        supplier_id: int | None = None,
        exclude_brands: list[str] | None = None,
        exclude_title_keywords: list[str] | None = None,
        min_cost: float | None = None,
        max_cost: float | None = None,
    ) -> dict:
        settings = await self.config_service.get_pipeline_settings()
        rules = await self.config_service.get_research_rules(
            supplier_id=supplier_id
        )
        batch_limit = (
            limit
            if limit is not None
            else settings.default_batch_size
        )
        priority_score = (
            min_priority_score
            if min_priority_score is not None
            else float(rules.min_priority_score)
        )

        amazon_service = AmazonMatchService(self.db)
        effective_exclude_brands = (
            exclude_brands
            if exclude_brands is not None
            else rules.lookup_excluded_brands
        )
        effective_exclude_keywords = (
            exclude_title_keywords
            if exclude_title_keywords is not None
            else rules.lookup_excluded_title_keywords
        )
        effective_min_cost = (
            min_cost
            if min_cost is not None
            else (
                float(rules.lookup_min_cost)
                if rules.lookup_min_cost is not None
                else None
            )
        )
        effective_max_cost = (
            max_cost
            if max_cost is not None
            else (
                float(rules.lookup_max_cost)
                if rules.lookup_max_cost is not None
                else None
            )
        )
        preview = await amazon_service.preview_pending_matches(
            min_priority_score=priority_score,
            limit=batch_limit,
            supplier_id=supplier_id,
            exclude_brands=effective_exclude_brands,
            exclude_title_keywords=effective_exclude_keywords,
            min_cost=effective_min_cost,
            max_cost=effective_max_cost,
        )

        return {
            "status": "ok",
            "settings": {
                "limit": batch_limit,
                "min_priority_score": priority_score,
                "use_real_keepa": settings.use_real_keepa,
                "marketplace": settings.default_marketplace,
                "supplier_id": supplier_id,
            },
            **preview,
        }
