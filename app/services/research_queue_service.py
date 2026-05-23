from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.supplier_offer import SupplierOffer
from app.models.offer_research_queue import OfferResearchQueue


class ResearchQueueService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def calculate_priority_score(self, offer: SupplierOffer) -> float:
        score = 0.0

        if offer.stock is not None:
            if offer.stock >= 20:
                score += 30
            elif offer.stock >= 10:
                score += 20
            elif offer.stock >= 3:
                score += 10
            elif offer.stock <= 1:
                score -= 20

        if offer.cost is not None:
            cost = float(offer.cost)

            if 20 <= cost <= 300:
                score += 30
            elif 300 < cost <= 1000:
                score += 15
            elif cost > 1000:
                score -= 10
            elif cost < 5:
                score -= 20

        if offer.brand:
            score += 15

        if offer.title:
            score += 15

        if offer.ean:
            score += 10

        return score

    async def populate_queue_from_supplier_offers(self) -> int:
        existing_offer_ids_subquery = select(
            OfferResearchQueue.supplier_offer_id
        )

        query = (
            select(SupplierOffer)
            .where(SupplierOffer.ean.is_not(None))
            .where(SupplierOffer.ean != "")
            .where(SupplierOffer.cost.is_not(None))
            .where(SupplierOffer.stock > 0)
            .where(SupplierOffer.id.not_in(existing_offer_ids_subquery))
        )

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
                "priority_score": self.calculate_priority_score(offer),
                "rejection_reason": None,
            }
            for offer in offers
        ]

        await self.db.execute(insert(OfferResearchQueue), rows)
        await self.db.commit()

        return len(rows)

    async def recalculate_priority_scores(self) -> int:
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
            queue_item.priority_score = self.calculate_priority_score(offer)
            updated += 1

        await self.db.commit()

        return updated

    async def list_queue(
        self,
        status: str | None = None,
        min_priority_score: float | None = None,
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
        )

        if status:
            query = query.where(OfferResearchQueue.status == status)

        if min_priority_score is not None:
            query = query.where(
                OfferResearchQueue.priority_score >= min_priority_score
            )

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