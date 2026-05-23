from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.amazon_product_match import AmazonProductMatch
from app.models.keepa_product_metric import KeepaProductMetric


class KeepaService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_pending_metrics(
        self,
        limit: int = 100,
    ) -> int:
        """
        Create Keepa tasks from matched ASINs.
        """

        existing_asins_subquery = select(
            KeepaProductMetric.asin
        )

        query = (
            select(AmazonProductMatch)
            .where(
                AmazonProductMatch.match_status == "matched"
            )
            .where(
                AmazonProductMatch.asin.is_not(None)
            )
            .where(
                AmazonProductMatch.asin.not_in(
                    existing_asins_subquery
                )
            )
            .order_by(
                AmazonProductMatch.created_at.desc()
            )
            .limit(limit)
        )

        result = await self.db.execute(query)
        matches = result.scalars().all()

        if not matches:
            return 0

        rows = []

        for match in matches:
            rows.append(
                {
                    "asin": match.asin,
                    "data_status": "pending",
                    "buy_box_price": None,
                    "currency": None,
                    "sales_rank": None,
                    "amazon_in_stock": None,
                    "estimated_monthly_sales": None,
                    "raw_data": None,
                }
            )

        await self.db.execute(
            insert(
                KeepaProductMetric
            ),
            rows,
        )

        await self.db.commit()

        return len(rows)

    async def process_pending_metrics(
        self,
        limit: int = 50,
    ) -> dict:
        """
        Temporary mock Keepa processor.
        Later replaced with real Keepa API.
        """

        query = (
            select(
                KeepaProductMetric
            )
            .where(
                KeepaProductMetric.data_status == "pending"
            )
            .limit(limit)
        )

        result = await self.db.execute(query)
        metrics = result.scalars().all()

        processed = 0

        for metric in metrics:

            # Mock data
            metric.buy_box_price = 199.99
            metric.currency = "EUR"
            metric.sales_rank = 12500
            metric.amazon_in_stock = True
            metric.estimated_monthly_sales = 85
            metric.data_status = "completed"

            metric.raw_data = {
                "mock": True,
                "source": "keepa_mock"
            }

            processed += 1

        await self.db.commit()

        return {
            "processed_count": processed
        }

    async def list_metrics(
        self,
        data_status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ):

        query = select(
            KeepaProductMetric
        )

        if data_status:
            query = query.where(
                KeepaProductMetric.data_status == data_status
            )

        query = (
            query
            .order_by(
                KeepaProductMetric.created_at.desc()
            )
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(query)

        metrics = result.scalars().all()

        return [
            {
                "asin": m.asin,
                "buy_box_price": (
                    float(m.buy_box_price)
                    if m.buy_box_price
                    else None
                ),
                "currency": m.currency,
                "sales_rank": m.sales_rank,
                "amazon_in_stock": m.amazon_in_stock,
                "estimated_monthly_sales": m.estimated_monthly_sales,
                "data_status": m.data_status,
            }
            for m in metrics
        ]