from datetime import datetime
import re

from sqlalchemy import func, insert, select
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

    def normalize_filter_terms(
        self,
        values: list[str] | None = None,
    ) -> list[str]:
        terms = []

        for value in values or []:
            for part in str(value or "").split(","):
                term = part.strip()

                if term:
                    terms.append(term)

        return sorted(set(terms), key=str.casefold)

    def pending_match_query(
        self,
        min_priority_score: float,
        supplier_id: int | None = None,
        exclude_brands: list[str] | None = None,
        exclude_title_keywords: list[str] | None = None,
        min_cost: float | None = None,
        max_cost: float | None = None,
    ):
        excluded_brands = self.normalize_filter_terms(exclude_brands)
        excluded_keywords = self.normalize_filter_terms(exclude_title_keywords)
        existing_queue_ids_subquery = select(
            AmazonProductMatch.queue_id
        )

        query = (
            select(
                OfferResearchQueue,
                SupplierOffer,
                Supplier.name.label("supplier_name"),
            )
            .join(
                SupplierOffer,
                SupplierOffer.id == OfferResearchQueue.supplier_offer_id,
            )
            .join(
                Supplier,
                Supplier.id == OfferResearchQueue.supplier_id,
            )
            .where(OfferResearchQueue.status == "needs_amazon_match")
            .where(OfferResearchQueue.priority_score >= min_priority_score)
            .where(OfferResearchQueue.id.not_in(existing_queue_ids_subquery))
        )

        if supplier_id is not None:
            query = query.where(OfferResearchQueue.supplier_id == supplier_id)
        else:
            query = query.where(Supplier.is_visible.is_(True))

        for brand in excluded_brands:
            query = query.where(
                (SupplierOffer.brand.is_(None))
                | (~SupplierOffer.brand.ilike(f"%{brand}%"))
            )

        for keyword in excluded_keywords:
            query = query.where(
                (SupplierOffer.title.is_(None))
                | (~SupplierOffer.title.ilike(f"%{keyword}%"))
            )

        if min_cost is not None:
            query = query.where(SupplierOffer.cost >= min_cost)

        if max_cost is not None:
            query = query.where(SupplierOffer.cost <= max_cost)

        return query

    def title_keywords(
        self,
        titles: list[str | None],
        limit: int = 12,
    ) -> list[dict]:
        counts: dict[str, int] = {}

        for title in titles:
            seen = set()

            for token in re.findall(r"[A-Za-zÀ-ž0-9]+", str(title or "").lower()):
                if len(token) < 4:
                    continue

                seen.add(token)

            for token in seen:
                counts[token] = counts.get(token, 0) + 1

        return [
            {
                "value": value,
                "count": count,
            }
            for value, count in sorted(
                counts.items(),
                key=lambda item: (-item[1], item[0]),
            )[:limit]
        ]

    async def preview_pending_matches(
        self,
        min_priority_score: float | None = None,
        limit: int | None = None,
        supplier_id: int | None = None,
        exclude_brands: list[str] | None = None,
        exclude_title_keywords: list[str] | None = None,
        min_cost: float | None = None,
        max_cost: float | None = None,
    ) -> dict:
        config_service = ConfigService(self.db)
        settings = None
        rules = None

        if limit is None:
            settings = await config_service.get_pipeline_settings()

        if min_priority_score is None:
            rules = await config_service.get_research_rules(
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
        excluded_brands = self.normalize_filter_terms(exclude_brands)
        excluded_keywords = self.normalize_filter_terms(exclude_title_keywords)

        base_query = self.pending_match_query(
            min_priority_score=priority_score,
            supplier_id=supplier_id,
            exclude_brands=excluded_brands,
            exclude_title_keywords=excluded_keywords,
            min_cost=min_cost,
            max_cost=max_cost,
        )
        total_result = await self.db.execute(
            select(func.count()).select_from(base_query.subquery())
        )
        total_eligible = int(total_result.scalar() or 0)

        batch_query = (
            base_query
            .order_by(
                OfferResearchQueue.priority_score.desc().nullslast(),
                OfferResearchQueue.created_at.desc(),
            )
            .limit(batch_limit)
        )
        result = await self.db.execute(batch_query)
        rows = result.all()

        brands: dict[str, int] = {}
        titles = []
        sample = []

        for queue_item, offer, supplier_name in rows:
            if offer.brand:
                brands[offer.brand] = brands.get(offer.brand, 0) + 1

            titles.append(offer.title)

            if len(sample) < 10:
                sample.append(
                    {
                        "supplier_name": supplier_name,
                        "ean": offer.ean,
                        "brand": offer.brand,
                        "title": offer.title,
                        "cost": (
                            float(offer.cost)
                            if offer.cost is not None
                            else None
                        ),
                        "currency": offer.currency,
                        "priority_score": (
                            float(queue_item.priority_score)
                            if queue_item.priority_score is not None
                            else None
                        ),
                    }
                )

        top_brands = [
            {
                "value": value,
                "count": count,
            }
            for value, count in sorted(
                brands.items(),
                key=lambda item: (-item[1], item[0] or ""),
            )[:12]
        ]
        costs = [
            float(offer.cost)
            for _queue_item, offer, _supplier_name in rows
            if offer.cost is not None
        ]

        return {
            "supplier_id": supplier_id,
            "min_priority_score": priority_score,
            "limit": batch_limit,
            "total_eligible": total_eligible,
            "will_request": len(rows),
            "estimated_external_requests": len(rows),
            "external_filters": {
                "exclude_brands": excluded_brands,
                "exclude_title_keywords": excluded_keywords,
                "min_cost": min_cost,
                "max_cost": max_cost,
            },
            "price": {
                "min": min(costs) if costs else None,
                "max": max(costs) if costs else None,
            },
            "top_brands": top_brands,
            "top_title_keywords": self.title_keywords(titles),
            "sample": sample,
        }

    async def create_pending_matches(
        self,
        min_priority_score: float | None = None,
        limit: int | None = None,
        supplier_id: int | None = None,
        exclude_brands: list[str] | None = None,
        exclude_title_keywords: list[str] | None = None,
        min_cost: float | None = None,
        max_cost: float | None = None,
    ) -> int:
        config_service = ConfigService(self.db)
        settings = None
        rules = None

        if limit is None:
            settings = await config_service.get_pipeline_settings()

        if min_priority_score is None:
            rules = await config_service.get_research_rules(
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
        excluded_brands = self.normalize_filter_terms(exclude_brands)
        excluded_keywords = self.normalize_filter_terms(exclude_title_keywords)

        query = (
            self.pending_match_query(
                min_priority_score=priority_score,
                supplier_id=supplier_id,
                exclude_brands=excluded_brands,
                exclude_title_keywords=excluded_keywords,
                min_cost=min_cost,
                max_cost=max_cost,
            )
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

        for queue_item, offer, _supplier_name in rows:
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
        else:
            query = query.where(Supplier.is_visible.is_(True))

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
