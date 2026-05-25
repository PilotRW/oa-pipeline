from decimal import Decimal

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.offer_research_queue import OfferResearchQueue
from app.models.research_rule import ResearchRule
from app.models.supplier import Supplier
from app.models.supplier_offer import SupplierOffer
from app.services.config_service import ConfigService


class ResearchQueueService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def calculate_priority_score(
        self,
        offer: SupplierOffer,
        rules: ResearchRule,
    ) -> float:
        score = 0.0

        if offer.stock is not None:
            if offer.stock >= rules.high_stock_threshold:
                score += rules.score_stock_high
            elif offer.stock >= rules.medium_stock_threshold:
                score += rules.score_stock_medium
            elif offer.stock > rules.low_stock_threshold:
                score += rules.score_stock_low
            elif offer.stock <= rules.low_stock_threshold:
                score += rules.score_stock_very_low

        if offer.cost is not None:
            cost = Decimal(str(offer.cost))

            if rules.preferred_cost_min <= cost <= rules.preferred_cost_max:
                score += rules.score_cost_preferred
            elif rules.preferred_cost_max < cost <= rules.medium_cost_max:
                score += rules.score_cost_medium
            elif cost > rules.medium_cost_max:
                score += rules.score_cost_high
            elif cost < rules.min_cost:
                score += rules.score_cost_low

        if offer.brand:
            score += rules.score_brand_present

        if offer.title:
            score += rules.score_title_present

        if offer.ean:
            score += rules.score_ean_present

        return float(score)

    async def populate_queue_from_supplier_offers(
        self,
        supplier_id: int | None = None,
    ) -> int:
        config_service = ConfigService(self.db)
        rules = await config_service.get_research_rules()

        existing_offer_ids_subquery = select(
            OfferResearchQueue.supplier_offer_id
        )

        query = (
            select(SupplierOffer)
            .where(SupplierOffer.ean.is_not(None))
            .where(SupplierOffer.ean != "")
            .where(SupplierOffer.cost.is_not(None))
            .where(SupplierOffer.id.not_in(existing_offer_ids_subquery))
        )

        if supplier_id is not None:
            query = query.where(SupplierOffer.supplier_id == supplier_id)

        result = await self.db.execute(query)
        offers = result.scalars().all()

        if not offers:
            return 0

        rows = [
            {
                "supplier_offer_id": offer.id,
                "supplier_id": offer.supplier_id,
                "ean": offer.ean,
                "status": "needs_amazon_match",
                "priority_score": self.calculate_priority_score(
                    offer=offer,
                    rules=rules,
                ),
                "rejection_reason": None,
            }
            for offer in offers
        ]

        await self.db.execute(
            insert(OfferResearchQueue),
            rows,
        )

        await self.db.commit()

        return len(rows)

    async def recalculate_priority_scores(self) -> int:
        config_service = ConfigService(self.db)
        rules = await config_service.get_research_rules()

        query = (
            select(OfferResearchQueue, SupplierOffer)
            .join(
                SupplierOffer,
                SupplierOffer.id == OfferResearchQueue.supplier_offer_id,
            )
        )

        result = await self.db.execute(query)
        rows = result.all()

        updated = 0

        for queue_item, offer in rows:
            queue_item.priority_score = self.calculate_priority_score(
                offer=offer,
                rules=rules,
            )
            updated += 1

        await self.db.commit()

        return updated

    async def list_queue(
        self,
        status: str | None = None,
        min_priority_score: float | None = None,
        supplier_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict]:
        query = (
            select(
                OfferResearchQueue.id.label("queue_id"),
                OfferResearchQueue.status,
                OfferResearchQueue.priority_score,
                OfferResearchQueue.rejection_reason,
                OfferResearchQueue.created_at,
                OfferResearchQueue.updated_at,
                OfferResearchQueue.supplier_offer_id,
                OfferResearchQueue.supplier_id,
                Supplier.name.label("supplier_name"),
                OfferResearchQueue.ean,
                SupplierOffer.supplier_sku,
                SupplierOffer.brand,
                SupplierOffer.title,
                SupplierOffer.cost,
                SupplierOffer.currency,
                SupplierOffer.stock,
            )
            .join(
                SupplierOffer,
                SupplierOffer.id == OfferResearchQueue.supplier_offer_id,
            )
            .join(
                Supplier,
                Supplier.id == OfferResearchQueue.supplier_id,
            )
        )

        if status:
            query = query.where(
                OfferResearchQueue.status == status
            )

        if min_priority_score is not None:
            query = query.where(
                OfferResearchQueue.priority_score >= min_priority_score
            )

        if supplier_id is not None:
            query = query.where(
                OfferResearchQueue.supplier_id == supplier_id
            )
        else:
            query = query.where(Supplier.is_visible.is_(True))

        query = (
            query
            .order_by(
                OfferResearchQueue.priority_score.desc().nullslast(),
                OfferResearchQueue.created_at.desc(),
            )
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(query)
        rows = result.mappings().all()

        return [
            {
                "queue_id": row["queue_id"],
                "status": row["status"],
                "priority_score": (
                    float(row["priority_score"])
                    if row["priority_score"] is not None
                    else None
                ),
                "rejection_reason": row["rejection_reason"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "supplier_offer_id": row["supplier_offer_id"],
                "supplier_id": row["supplier_id"],
                "supplier_name": row["supplier_name"],
                "ean": row["ean"],
                "supplier_sku": row["supplier_sku"],
                "brand": row["brand"],
                "title": row["title"],
                "cost": (
                    float(row["cost"])
                    if row["cost"] is not None
                    else None
                ),
                "currency": row["currency"],
                "stock": row["stock"],
            }
            for row in rows
        ]
