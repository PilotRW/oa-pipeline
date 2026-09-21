from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings as app_settings
from app.models.amazon_product_match import AmazonProductMatch
from app.models.market_snapshot import MarketSnapshot
from app.models.offer_research_queue import OfferResearchQueue
from app.models.supplier import Supplier
from app.models.supplier_offer import SupplierOffer
from app.services.config_service import ConfigService
from app.services.keepa_client import (
    KeepaConfigurationError,
    KeepaMetricsClient,
    KeepaRateLimitError,
)
from app.services.keepa_batch_policy import effective_batch_limit
from app.services.marketplace import currency_for_marketplace
from app.services.provider_result_mappers import apply_market_snapshot_result


class MarketSnapshotService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_pending_snapshots(
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

        existing_match_ids_subquery = select(
            MarketSnapshot.amazon_product_match_id
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
            .where(
                AmazonProductMatch.id.not_in(
                    existing_match_ids_subquery
                )
            )
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
                    "amazon_product_match_id": match.id,
                    "queue_id": match.queue_id,
                    "supplier_offer_id": match.supplier_offer_id,
                    "asin": match.asin,
                    "marketplace": None,
                    "current_price": None,
                    "buy_box_price": None,
                    "buy_box_exists": None,
                    "sales_rank": None,
                    "seller_count": None,
                    "amazon_present": None,
                    "fba_fee_estimate": None,
                    "estimated_monthly_sales": None,
                    "snapshot_source": None,
                    "snapshot_status": "pending",
                    "error_message": None,
                    "raw_data": None,
                }
            )

            queue_item.status = "market_snapshot_pending"

        await self.db.execute(
            insert(MarketSnapshot),
            rows,
        )

        await self.db.commit()

        return len(rows)

    async def process_pending_snapshots(
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
        requested_limit = batch_limit
        token_cost_per_item = 0
        token_status = None
        processed = 0

        if real_keepa_enabled:
            token_cost_per_item = (
                KeepaMetricsClient.product_query_token_cost(
                    include_buybox=False
                )
            )
            try:
                client = KeepaMetricsClient()
                token_status = await client.get_token_status()
            except KeepaConfigurationError as exc:
                return {
                    "processed_count": processed,
                    "data_source": "keepa_real",
                    "status": "not_configured",
                    "reason": str(exc),
                    "requested_limit": requested_limit,
                    "effective_limit": 0,
                    "token_cost_per_item": token_cost_per_item,
                    "token_status": token_status,
                }

            batch_limit = effective_batch_limit(
                batch_limit,
                tokens_left=token_status["tokens_left"],
                token_cost_per_item=token_cost_per_item,
                configured_limit=app_settings.KEEPA_REAL_BATCH_LIMIT,
            )

            if batch_limit < 1:
                return {
                    "processed_count": processed,
                    "data_source": "keepa_real",
                    "status": "rate_limited",
                    "reason": "Not enough Keepa API tokens",
                    "requested_limit": requested_limit,
                    "effective_limit": 0,
                    "token_cost_per_item": token_cost_per_item,
                    "token_status": token_status,
                }

        query = (
            select(
                MarketSnapshot,
                OfferResearchQueue,
            )
            .join(
                OfferResearchQueue,
                OfferResearchQueue.id == MarketSnapshot.queue_id,
            )
            .where(MarketSnapshot.snapshot_status == "pending")
        )

        if supplier_id is not None:
            query = (
                query
                .join(
                    SupplierOffer,
                    SupplierOffer.id == MarketSnapshot.supplier_offer_id,
                )
                .where(SupplierOffer.supplier_id == supplier_id)
            )

        query = query.limit(batch_limit)

        result = await self.db.execute(query)
        rows = result.all()

        if real_keepa_enabled:
            not_found = 0

            for snapshot, queue_item in rows:
                try:
                    snapshot_result = await client.fetch_market_snapshot(
                        asin=snapshot.asin,
                        marketplace=target_marketplace,
                    )
                except KeepaRateLimitError as exc:
                    await self.db.commit()

                    return {
                        "processed_count": processed,
                        "data_source": "keepa_real",
                        "not_found_count": not_found,
                        "status": "rate_limited",
                        "reason": str(exc),
                        "requested_limit": requested_limit,
                        "effective_limit": batch_limit,
                        "token_cost_per_item": token_cost_per_item,
                        "token_status": token_status,
                    }

                if not snapshot_result:
                    snapshot.snapshot_status = "not_found"
                    snapshot.snapshot_source = "keepa_real"
                    queue_item.status = "market_snapshot_not_found"
                    not_found += 1
                    continue

                self.apply_snapshot_result(
                    snapshot=snapshot,
                    result=snapshot_result,
                )
                snapshot.snapshot_status = "completed"
                queue_item.status = "market_snapshot_completed"

                processed += 1

            await self.db.commit()

            return {
                "processed_count": processed,
                "data_source": "keepa_real",
                "not_found_count": not_found,
                "requested_limit": requested_limit,
                "effective_limit": batch_limit,
                "token_cost_per_item": token_cost_per_item,
                "token_status": token_status,
                "status": "ok",
            }

        for snapshot, queue_item in rows:
            self.apply_snapshot_result(
                snapshot=snapshot,
                result={
                    "marketplace": target_marketplace,
                    "current_price": 199.99,
                    "buy_box_price": 199.99,
                    "buy_box_exists": True,
                    "sales_rank": 12500,
                    "seller_count": 8,
                    "amazon_present": True,
                    "fba_fee_estimate": None,
                    "estimated_monthly_sales": 85,
                    "snapshot_source": "market_snapshot_mock",
                    "raw_data": {
                        "mock": True,
                        "source": "market_snapshot_mock",
                        "currency": currency_for_marketplace(
                            target_marketplace
                        ),
                    },
                },
            )
            snapshot.snapshot_status = "completed"
            queue_item.status = "market_snapshot_completed"

            processed += 1

        await self.db.commit()

        return {
            "processed_count": processed,
            "data_source": "market_snapshot_mock",
            "status": "ok",
        }

    def apply_snapshot_result(
        self,
        snapshot: MarketSnapshot,
        result: dict,
    ) -> None:
        apply_market_snapshot_result(snapshot, result)

    async def list_snapshots(
        self,
        snapshot_status: str | None = None,
        supplier_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict]:
        query = (
            select(
                MarketSnapshot,
                Supplier.name.label("supplier_name"),
            )
            .join(
                SupplierOffer,
                SupplierOffer.id == MarketSnapshot.supplier_offer_id,
            )
            .join(
                Supplier,
                Supplier.id == SupplierOffer.supplier_id,
            )
        )

        if snapshot_status:
            query = query.where(
                MarketSnapshot.snapshot_status == snapshot_status
            )

        if supplier_id is not None:
            query = query.where(
                SupplierOffer.supplier_id == supplier_id
            )
        else:
            query = query.where(Supplier.is_visible.is_(True))

        query = (
            query
            .order_by(MarketSnapshot.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(query)
        rows = result.all()

        return [
            {
                "id": snapshot.id,
                "supplier_name": supplier_name,
                "amazon_product_match_id": snapshot.amazon_product_match_id,
                "queue_id": snapshot.queue_id,
                "supplier_offer_id": snapshot.supplier_offer_id,
                "asin": snapshot.asin,
                "marketplace": snapshot.marketplace,
                "current_price": (
                    float(snapshot.current_price)
                    if snapshot.current_price is not None
                    else None
                ),
                "buy_box_price": (
                    float(snapshot.buy_box_price)
                    if snapshot.buy_box_price is not None
                    else None
                ),
                "buy_box_exists": snapshot.buy_box_exists,
                "sales_rank": snapshot.sales_rank,
                "seller_count": snapshot.seller_count,
                "amazon_present": snapshot.amazon_present,
                "fba_fee_estimate": (
                    float(snapshot.fba_fee_estimate)
                    if snapshot.fba_fee_estimate is not None
                    else None
                ),
                "estimated_monthly_sales": snapshot.estimated_monthly_sales,
                "snapshot_source": snapshot.snapshot_source,
                "snapshot_status": snapshot.snapshot_status,
                "error_message": snapshot.error_message,
                "created_at": snapshot.created_at,
                "updated_at": snapshot.updated_at,
            }
            for snapshot, supplier_name in rows
        ]
