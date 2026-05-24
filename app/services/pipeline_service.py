from sqlalchemy.ext.asyncio import AsyncSession

from app.services.amazon_match_service import AmazonMatchService
from app.services.config_service import ConfigService
from app.services.deal_service import DealService
from app.services.keepa_service import KeepaService


class PipelineService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.config_service = ConfigService(db)

    async def run_batch(
        self,
        min_priority_score: float | None = None,
        limit: int | None = None,
    ) -> dict:
        settings = await self.config_service.get_pipeline_settings()
        rules = await self.config_service.get_research_rules()

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
        )

        amazon_processed = await amazon_service.process_pending_matches(
            limit=batch_limit,
        )

        keepa_pending_created = await keepa_service.create_pending_metrics(
            limit=batch_limit,
        )

        keepa_processed = await keepa_service.process_pending_metrics(
            limit=batch_limit,
            use_real_keepa=settings.use_real_keepa,
            marketplace=settings.default_marketplace,
        )

        deal_candidates_created = await deal_service.create_deal_candidates(
            limit=batch_limit,
        )

        return {
            "status": "ok",
            "settings": {
                "limit": batch_limit,
                "min_priority_score": priority_score,
                "use_real_keepa": settings.use_real_keepa,
                "marketplace": settings.default_marketplace,
            },
            "amazon_pending_created": amazon_pending_created,
            "amazon_processed": amazon_processed,
            "keepa_pending_created": keepa_pending_created,
            "keepa_processed": keepa_processed,
            "deal_candidates_created": deal_candidates_created,
        }
