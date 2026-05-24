from decimal import Decimal

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.amazon_product_match import AmazonProductMatch
from app.models.deal_candidate import DealCandidate
from app.models.keepa_product_metric import KeepaProductMetric
from app.models.offer_research_queue import OfferResearchQueue
from app.models.research_rule import ResearchRule
from app.models.supplier_offer import SupplierOffer
from app.services.config_service import ConfigService


class DealService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def estimate_fees(
        self,
        amazon_price: Decimal,
        rules: ResearchRule,
    ) -> Decimal:
        referral_fee = (
            amazon_price
            * Decimal(str(rules.referral_fee_percent))
            / Decimal("100.00")
        )
        fulfillment_fee = Decimal(str(rules.fulfillment_fee_fixed))

        return referral_fee + fulfillment_fee

    def calculate_profit(
        self,
        amazon_price: Decimal,
        supplier_cost: Decimal,
        estimated_fees: Decimal,
    ) -> Decimal:
        return amazon_price - supplier_cost - estimated_fees

    def calculate_roi(
        self,
        profit: Decimal,
        supplier_cost: Decimal,
    ) -> Decimal:
        if supplier_cost <= 0:
            return Decimal("0.00")

        return (profit / supplier_cost) * Decimal("100.00")

    async def create_deal_candidates(
        self,
        limit: int | None = None,
    ) -> int:
        settings = None

        if limit is None:
            settings = await ConfigService(
                self.db
            ).get_pipeline_settings()

        batch_limit = (
            limit
            if limit is not None
            else settings.default_batch_size
        )

        existing_offer_ids_subquery = select(
            DealCandidate.supplier_offer_id
        )

        query = (
            select(
                AmazonProductMatch,
                KeepaProductMetric,
                SupplierOffer,
                OfferResearchQueue,
            )
            .join(
                KeepaProductMetric,
                KeepaProductMetric.asin == AmazonProductMatch.asin,
            )
            .join(
                SupplierOffer,
                SupplierOffer.id == AmazonProductMatch.supplier_offer_id,
            )
            .join(
                OfferResearchQueue,
                OfferResearchQueue.id == AmazonProductMatch.queue_id,
            )
            .where(AmazonProductMatch.match_status == "matched")
            .where(KeepaProductMetric.data_status == "completed")
            .where(SupplierOffer.id.not_in(existing_offer_ids_subquery))
            .limit(batch_limit)
        )

        result = await self.db.execute(query)
        rows = result.all()

        if not rows:
            return 0

        rules = await ConfigService(
            self.db
        ).get_research_rules()

        deal_rows = []

        for match, keepa, offer, queue_item in rows:
            if keepa.buy_box_price is None or offer.cost is None:
                continue

            amazon_price = Decimal(str(keepa.buy_box_price))
            supplier_cost = Decimal(str(offer.cost))

            estimated_fees = self.estimate_fees(
                amazon_price=amazon_price,
                rules=rules,
            )

            estimated_profit = self.calculate_profit(
                amazon_price=amazon_price,
                supplier_cost=supplier_cost,
                estimated_fees=estimated_fees,
            )

            roi_percent = self.calculate_roi(
                profit=estimated_profit,
                supplier_cost=supplier_cost,
            )

            status = "candidate"
            rejection_reason = None

            if estimated_profit <= rules.min_profit:
                status = "rejected_unprofitable"
                rejection_reason = (
                    f"Profit below {rules.min_profit}"
                )

            elif roi_percent < rules.min_roi_percent:
                status = "rejected_low_roi"
                rejection_reason = (
                    f"ROI below {rules.min_roi_percent}%"
                )

            elif (
                rules.max_sales_rank is not None
                and keepa.sales_rank is not None
                and keepa.sales_rank > rules.max_sales_rank
            ):
                status = "rejected_low_roi"
                rejection_reason = (
                    f"Sales rank above {rules.max_sales_rank}"
                )

            elif (
                rules.min_monthly_sales is not None
                and keepa.estimated_monthly_sales is not None
                and keepa.estimated_monthly_sales
                < rules.min_monthly_sales
            ):
                status = "rejected_low_roi"
                rejection_reason = (
                    f"Monthly sales below {rules.min_monthly_sales}"
                )

            elif (
                rules.exclude_amazon_in_stock
                and keepa.amazon_in_stock
            ):
                status = "rejected_low_roi"
                rejection_reason = "Amazon in stock"

            if status == "candidate":
                queue_item.status = "deal_candidate"

            elif status == "rejected_low_roi":
                queue_item.status = "rejected_low_roi"

            elif status == "rejected_unprofitable":
                queue_item.status = "rejected_unprofitable"

            queue_item.rejection_reason = rejection_reason

            deal_rows.append(
                {
                    "supplier_offer_id": offer.id,
                    "asin": match.asin,
                    "supplier_cost": supplier_cost,
                    "amazon_price": amazon_price,
                    "estimated_fees": estimated_fees,
                    "estimated_profit": estimated_profit,
                    "roi_percent": roi_percent,
                    "sales_rank": keepa.sales_rank,
                    "estimated_monthly_sales": keepa.estimated_monthly_sales,
                    "status": status,
                }
            )

        if not deal_rows:
            return 0

        await self.db.execute(
            insert(DealCandidate),
            deal_rows,
        )

        await self.db.commit()

        return len(deal_rows)

    async def list_deal_candidates(
        self,
        status: str | None = None,
        min_roi_percent: float | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict]:
        query = select(
            DealCandidate
        )

        if status:
            query = query.where(
                DealCandidate.status == status
            )

        if min_roi_percent is not None:
            query = query.where(
                DealCandidate.roi_percent >= min_roi_percent
            )

        query = (
            query
            .order_by(
                DealCandidate.roi_percent.desc().nullslast(),
                DealCandidate.created_at.desc(),
            )
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(query)
        deals = result.scalars().all()

        return [
            {
                "id": deal.id,
                "supplier_offer_id": deal.supplier_offer_id,
                "asin": deal.asin,
                "supplier_cost": float(deal.supplier_cost),
                "amazon_price": (
                    float(deal.amazon_price)
                    if deal.amazon_price is not None
                    else None
                ),
                "estimated_fees": (
                    float(deal.estimated_fees)
                    if deal.estimated_fees is not None
                    else None
                ),
                "estimated_profit": (
                    float(deal.estimated_profit)
                    if deal.estimated_profit is not None
                    else None
                ),
                "roi_percent": (
                    float(deal.roi_percent)
                    if deal.roi_percent is not None
                    else None
                ),
                "sales_rank": deal.sales_rank,
                "estimated_monthly_sales": deal.estimated_monthly_sales,
                "status": deal.status,
                "created_at": deal.created_at,
                "updated_at": deal.updated_at,
            }
            for deal in deals
        ]
