from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.amazon_product_match import AmazonProductMatch
from app.models.keepa_product_metric import KeepaProductMetric
from app.models.offer_research_queue import OfferResearchQueue
from app.models.supplier import Supplier
from app.models.supplier_offer import SupplierOffer
from app.services.config_service import ConfigService
from app.services.keepa_client import (
    KeepaConfigurationError,
    KeepaMetricsClient,
)
from app.services.marketplace import currency_for_marketplace


class KeepaService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_pending_metrics(
        self,
        limit: int | None = None,
        supplier_id: int | None = None,
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

        existing_asins_subquery = select(
            KeepaProductMetric.asin
        )

        query = (
            select(
                AmazonProductMatch,
                OfferResearchQueue,
            )
            .join(
                OfferResearchQueue,
                OfferResearchQueue.id == AmazonProductMatch.queue_id,
            )
            .where(AmazonProductMatch.match_status == "matched")
            .where(AmazonProductMatch.asin.is_not(None))
            .where(AmazonProductMatch.asin.not_in(existing_asins_subquery))
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
            AmazonProductMatch.created_at.desc()
        ).limit(batch_limit)

        result = await self.db.execute(query)
        rows_result = result.all()

        if not rows_result:
            return 0

        rows = []

        for match, queue_item in rows_result:
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

            queue_item.status = "keepa_pending"

        await self.db.execute(
            insert(KeepaProductMetric),
            rows,
        )

        await self.db.commit()

        return len(rows)

    async def process_pending_metrics(
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

        query = (
            select(
                KeepaProductMetric,
                AmazonProductMatch,
                OfferResearchQueue,
            )
            .join(
                AmazonProductMatch,
                AmazonProductMatch.asin == KeepaProductMetric.asin,
            )
            .join(
                OfferResearchQueue,
                OfferResearchQueue.id == AmazonProductMatch.queue_id,
            )
            .where(KeepaProductMetric.data_status == "pending")
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

        query = query.limit(batch_limit)

        result = await self.db.execute(query)
        rows = result.all()

        processed = 0

        if real_keepa_enabled:
            try:
                client = KeepaMetricsClient()
            except KeepaConfigurationError as exc:
                return {
                    "processed_count": processed,
                    "data_source": "keepa_real",
                    "status": "not_configured",
                    "reason": str(exc),
                }

            not_found = 0

            for metric, match, queue_item in rows:
                metric_result = await client.fetch_product_metrics(
                    asin=metric.asin,
                    marketplace=target_marketplace,
                )

                if not metric_result:
                    metric.data_status = "not_found"
                    queue_item.status = "keepa_not_found"
                    not_found += 1
                    continue

                metric.buy_box_price = metric_result["buy_box_price"]
                metric.currency = (
                    metric_result["currency"]
                    or currency_for_marketplace(target_marketplace)
                )
                metric.sales_rank = metric_result["sales_rank"]
                metric.amazon_in_stock = metric_result["amazon_in_stock"]
                metric.estimated_monthly_sales = (
                    metric_result["estimated_monthly_sales"]
                )
                metric.data_status = "completed"
                metric.raw_data = metric_result["raw_data"]

                queue_item.status = "keepa_completed"

                processed += 1

            await self.db.commit()

            return {
                "processed_count": processed,
                "data_source": "keepa_real",
                "not_found_count": not_found,
            }

        for metric, match, queue_item in rows:
            metric.buy_box_price = 199.99
            metric.currency = currency_for_marketplace(
                target_marketplace
            )
            metric.sales_rank = 12500
            metric.amazon_in_stock = True
            metric.estimated_monthly_sales = 85
            metric.data_status = "completed"
            metric.raw_data = {
                "mock": True,
                "source": "keepa_mock",
            }

            queue_item.status = "keepa_completed"

            processed += 1

        await self.db.commit()

        return {
            "processed_count": processed,
            "data_source": "keepa_mock",
        }

    async def list_metrics(
        self,
        data_status: str | None = None,
        supplier_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict]:
        query = (
            select(
                KeepaProductMetric,
                Supplier.name.label("supplier_name"),
            )
            .join(
                AmazonProductMatch,
                AmazonProductMatch.asin == KeepaProductMetric.asin,
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

        if data_status:
            query = query.where(
                KeepaProductMetric.data_status == data_status
            )

        if supplier_id is not None:
            query = query.where(
                SupplierOffer.supplier_id == supplier_id
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
        rows = result.all()

        return [
            {
                "asin": m.asin,
                "supplier_name": supplier_name,
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
            for m, supplier_name in rows
        ]
