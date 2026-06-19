from datetime import datetime, timezone

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.amazon_presence_check import AmazonPresenceCheck
from app.models.amazon_product_match import AmazonProductMatch
from app.models.keepa_product_metric import KeepaProductMetric
from app.models.supplier import Supplier
from app.models.supplier_offer import SupplierOffer
from app.services.config_service import ConfigService
from app.services.keepa_client import (
    KeepaConfigurationError,
    KeepaMetricsClient,
)


class AmazonPresenceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_pending_checks(
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
            AmazonPresenceCheck.amazon_product_match_id
        )

        query = (
            select(AmazonProductMatch)
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
        matches = result.scalars().all()

        if not matches:
            return 0

        rows = [
            {
                "amazon_product_match_id": match.id,
                "supplier_offer_id": match.supplier_offer_id,
                "asin": match.asin,
                "presence_status": "pending",
                "amazon_present": None,
                "data_source": None,
                "raw_data": None,
            }
            for match in matches
        ]

        await self.db.execute(
            insert(AmazonPresenceCheck),
            rows,
        )
        await self.db.commit()

        return len(rows)

    async def process_pending_checks(
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
            select(AmazonPresenceCheck)
            .where(AmazonPresenceCheck.presence_status == "pending")
        )

        if supplier_id is not None:
            query = (
                query
                .join(
                    SupplierOffer,
                    SupplierOffer.id == AmazonPresenceCheck.supplier_offer_id,
                )
                .where(SupplierOffer.supplier_id == supplier_id)
            )

        query = query.order_by(
            AmazonPresenceCheck.created_at.asc()
        ).limit(batch_limit)

        result = await self.db.execute(query)
        checks = result.scalars().all()

        processed = 0
        not_found = 0

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

            for check in checks:
                metric_result = await client.fetch_product_metrics(
                    asin=check.asin,
                    marketplace=target_marketplace,
                )

                if not metric_result:
                    check.presence_status = "not_found"
                    check.data_source = "keepa_real"
                    check.marketplace = target_marketplace
                    check.raw_data = {
                        "source": "keepa_real",
                        "reason": "product_not_found",
                    }
                    check.checked_at = datetime.now(timezone.utc)
                    not_found += 1
                    continue

                await self._complete_check(
                    check=check,
                    amazon_present=bool(metric_result["amazon_in_stock"]),
                    data_source="keepa_real",
                    marketplace=target_marketplace,
                    raw_data={
                        "source": "keepa_real",
                        "asin": metric_result["asin"],
                        "amazon_in_stock": metric_result["amazon_in_stock"],
                        "raw_data": metric_result["raw_data"],
                    },
                )
                processed += 1

            await self.db.commit()

            return {
                "processed_count": processed,
                "not_found_count": not_found,
                "data_source": "keepa_real",
                "status": "ok",
            }

        for check in checks:
            amazon_present = self.mock_amazon_presence(check.asin)
            await self._complete_check(
                check=check,
                amazon_present=amazon_present,
                data_source="presence_mock",
                marketplace=target_marketplace,
                raw_data={
                    "mock": True,
                    "source": "presence_mock",
                    "rule": "deterministic_asin_checksum",
                },
            )
            processed += 1

        await self.db.commit()

        return {
            "processed_count": processed,
            "data_source": "presence_mock",
            "status": "ok",
        }

    async def list_checks(
        self,
        presence_status: str | None = None,
        amazon_present: bool | None = None,
        supplier_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict]:
        query = (
            select(
                AmazonPresenceCheck,
                Supplier.name.label("supplier_name"),
                AmazonProductMatch.amazon_title.label("amazon_title"),
            )
            .join(
                AmazonProductMatch,
                AmazonProductMatch.id
                == AmazonPresenceCheck.amazon_product_match_id,
            )
            .join(
                SupplierOffer,
                SupplierOffer.id == AmazonPresenceCheck.supplier_offer_id,
            )
            .join(
                Supplier,
                Supplier.id == SupplierOffer.supplier_id,
            )
        )

        if presence_status:
            query = query.where(
                AmazonPresenceCheck.presence_status == presence_status
            )

        if amazon_present is not None:
            query = query.where(
                AmazonPresenceCheck.amazon_present.is_(amazon_present)
            )

        if supplier_id is not None:
            query = query.where(
                SupplierOffer.supplier_id == supplier_id
            )
        else:
            query = query.where(Supplier.is_visible.is_(True))

        query = (
            query
            .order_by(AmazonPresenceCheck.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(query)
        rows = result.all()

        return [
            {
                "id": check.id,
                "supplier_name": supplier_name,
                "asin": check.asin,
                "amazon_title": amazon_title,
                "amazon_present": check.amazon_present,
                "presence_status": check.presence_status,
                "data_source": check.data_source,
                "marketplace": check.marketplace,
                "checked_at": (
                    check.checked_at.isoformat()
                    if check.checked_at
                    else None
                ),
            }
            for check, supplier_name, amazon_title in rows
        ]

    async def _complete_check(
        self,
        *,
        check: AmazonPresenceCheck,
        amazon_present: bool,
        data_source: str,
        marketplace: str,
        raw_data: dict,
    ) -> None:
        check.amazon_present = amazon_present
        check.presence_status = "completed"
        check.data_source = data_source
        check.marketplace = marketplace
        check.raw_data = raw_data
        check.checked_at = datetime.now(timezone.utc)

        metric_result = await self.db.execute(
            select(KeepaProductMetric).where(
                KeepaProductMetric.asin == check.asin
            )
        )
        metric = metric_result.scalar_one_or_none()

        if metric is not None:
            metric.amazon_in_stock = amazon_present

    def mock_amazon_presence(
        self,
        asin: str,
    ) -> bool:
        checksum = sum(ord(character) for character in asin or "")

        return checksum % 3 == 0
