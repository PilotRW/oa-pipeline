from datetime import datetime

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.amazon_product_match import AmazonProductMatch
from app.models.offer_research_queue import OfferResearchQueue
from app.models.supplier import Supplier
from app.models.supplier_offer import SupplierOffer
from app.services.amazon_matchers.factory import get_amazon_matcher
from app.services.config_service import ConfigService
from app.services.keepa_client import KeepaConfigurationError


class AmazonMatchService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_pending_matches(
        self,
        min_priority_score: float | None = None,
        limit: int | None = None,
        supplier_id: int | None = None,
    ) -> int:
        config_service = ConfigService(self.db)
        settings = None
        rules = None

        if limit is None:
            settings = await config_service.get_pipeline_settings()

        if min_priority_score is None:
            rules = await config_service.get_research_rules()

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

        existing_queue_ids_subquery = select(
            AmazonProductMatch.queue_id
        )

        query = (
            select(
                OfferResearchQueue,
                SupplierOffer,
            )
            .join(
                SupplierOffer,
                SupplierOffer.id == OfferResearchQueue.supplier_offer_id,
            )
            .where(OfferResearchQueue.status == "needs_amazon_match")
            .where(OfferResearchQueue.priority_score >= priority_score)
            .where(OfferResearchQueue.id.not_in(existing_queue_ids_subquery))
        )

        if supplier_id is not None:
            query = query.where(OfferResearchQueue.supplier_id == supplier_id)

        query = (
            query
            .order_by(
                OfferResearchQueue.priority_score.desc().nullslast(),
                OfferResearchQueue.created_at.desc(),
            )
            .limit(batch_limit)
        )

        result = await self.db.execute(query)
        rows = result.all()

        if not rows:
            return 0

        match_rows = []

        for queue_item, offer in rows:
            match_rows.append(
                {
                    "queue_id": queue_item.id,
                    "supplier_offer_id": offer.id,
                    "ean": offer.ean,
                    "match_status": "pending",
                    "match_confidence": None,
                    "asin": None,
                    "amazon_title": None,
                    "amazon_brand": None,
                    "matched_at": None,
                }
            )

        await self.db.execute(insert(AmazonProductMatch), match_rows)
        await self.db.commit()

        return len(match_rows)

    async def process_pending_matches(
        self,
        limit: int | None = None,
        use_real_keepa: bool | None = None,
        marketplace: str | None = None,
        supplier_id: int | None = None,
    ) -> dict:
        settings = None

        if (
            limit is None
            or use_real_keepa is None
            or marketplace is None
        ):
            settings = await ConfigService(
                self.db
            ).get_pipeline_settings()

        batch_limit = (
            limit
            if limit is not None
            else settings.default_batch_size
        )
        real_keepa_enabled = (
            use_real_keepa
            if use_real_keepa is not None
            else settings.use_real_keepa
        )
        target_marketplace = (
            marketplace
            if marketplace is not None
            else settings.default_marketplace
        )

        try:
            matcher = get_amazon_matcher(
                use_real_keepa=real_keepa_enabled
            )
        except KeepaConfigurationError as exc:
            return {
                "processed_count": 0,
                "matched_count": 0,
                "not_found_count": 0,
                "data_source": "keepa_real",
                "status": "not_configured",
                "reason": str(exc),
            }

        query = select(AmazonProductMatch).where(
            AmazonProductMatch.match_status == "pending"
        )

        if supplier_id is not None:
            query = (
                query
                .join(
                    SupplierOffer,
                    SupplierOffer.id == AmazonProductMatch.supplier_offer_id,
                )
                .where(SupplierOffer.supplier_id == supplier_id)
            )

        query = query.order_by(
            AmazonProductMatch.created_at.asc()
        ).limit(batch_limit)

        result = await self.db.execute(query)
        matches = result.scalars().all()

        matched_count = 0
        not_found_count = 0

        for match in matches:
            match_result = await matcher.match_by_ean(
                match.ean,
                marketplace=target_marketplace,
            )

            queue_result = await self.db.execute(
                select(OfferResearchQueue).where(
                    OfferResearchQueue.id == match.queue_id
                )
            )
            queue_item = queue_result.scalar_one_or_none()

            if match_result:
                match.asin = match_result["asin"]
                match.amazon_title = match_result["amazon_title"]
                match.amazon_brand = match_result["amazon_brand"]
                match.match_confidence = match_result["match_confidence"]
                match.match_status = "matched"
                match.matched_at = datetime.utcnow()

                if queue_item:
                    queue_item.status = "matched"

                matched_count += 1
            else:
                match.match_status = "not_found"
                match.matched_at = datetime.utcnow()

                if queue_item:
                    queue_item.status = "amazon_match_not_found"

                not_found_count += 1

        await self.db.commit()

        return {
            "processed_count": len(matches),
            "matched_count": matched_count,
            "not_found_count": not_found_count,
            "data_source": (
                "keepa_real"
                if real_keepa_enabled
                else "mock"
            ),
        }

    async def list_matches(
        self,
        match_status: str | None = None,
        supplier_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict]:
        query = (
            select(
                AmazonProductMatch,
                Supplier.name.label("supplier_name"),
            )
            .join(
                SupplierOffer,
                SupplierOffer.id == AmazonProductMatch.supplier_offer_id,
            )
            .join(
                Supplier,
                Supplier.id == SupplierOffer.supplier_id,
            )
        )

        if match_status:
            query = query.where(
                AmazonProductMatch.match_status == match_status
            )

        if supplier_id is not None:
            query = query.where(
                SupplierOffer.supplier_id == supplier_id
            )

        query = (
            query
            .order_by(AmazonProductMatch.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(query)
        rows = result.all()

        return [
            {
                "id": match.id,
                "queue_id": match.queue_id,
                "supplier_offer_id": match.supplier_offer_id,
                "supplier_name": supplier_name,
                "ean": match.ean,
                "asin": match.asin,
                "match_status": match.match_status,
                "match_confidence": (
                    float(match.match_confidence)
                    if match.match_confidence is not None
                    else None
                ),
                "amazon_title": match.amazon_title,
                "amazon_brand": match.amazon_brand,
                "matched_at": match.matched_at,
                "created_at": match.created_at,
            }
            for match, supplier_name in rows
        ]
