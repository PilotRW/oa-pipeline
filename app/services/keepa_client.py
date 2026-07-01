import asyncio
from decimal import Decimal
from typing import Any

import keepa

from app.config.settings import settings
from app.services.marketplace import keepa_domain_for_marketplace


class KeepaConfigurationError(ValueError):
    pass


class KeepaRateLimitError(RuntimeError):
    pass


class KeepaMetricsClient:
    PRODUCT_QUERY_TOKEN_COST = 1
    BUYBOX_EXTRA_TOKEN_COST = 2

    @staticmethod
    def is_api_key_configured(
        api_key: str | None = None,
    ) -> bool:
        key = api_key or settings.KEEPA_API_KEY

        return bool(
            key
            and key != "your_keepa_api_key_here"
        )

    def __init__(
        self,
        api_key: str | None = None,
    ):
        self.api_key = api_key or settings.KEEPA_API_KEY

        if not self.is_api_key_configured(self.api_key):
            raise KeepaConfigurationError(
                "KEEPA_API_KEY is not configured"
            )

        self.api = keepa.Keepa(
            self.api_key,
            check_key=False,
        )

    async def fetch_product_metrics(
        self,
        asin: str,
        marketplace: str,
        include_buybox: bool = True,
    ) -> dict | None:
        if not asin:
            return None

        try:
            products = await asyncio.to_thread(
                self.api.query,
                asin,
                stats=30,
                domain=keepa_domain_for_marketplace(marketplace),
                history=False,
                product_code_is_asin=True,
                progress_bar=False,
                buybox=include_buybox,
                wait=False,
            )
        except RuntimeError as exc:
            if "NOT_ENOUGH_TOKEN" in str(exc):
                raise KeepaRateLimitError(str(exc)) from exc
            raise

        if not products:
            return None

        product = products[0]
        stats = product.get("stats") or {}
        current = stats.get("current") or {}

        buy_box_price = self.first_price(
            current,
            [
                "BUY_BOX_SHIPPING",
                "NEW_FBA",
                "NEW",
                "AMAZON",
            ],
        )

        sales_rank = self.int_or_none(
            current.get("SALES")
        )

        amazon_price = self.decimal_or_none(
            current.get("AMAZON")
        )

        return {
            "asin": product.get("asin") or asin,
            "buy_box_price": buy_box_price,
            "currency": product.get("currency"),
            "sales_rank": sales_rank,
            "amazon_in_stock": amazon_price is not None,
            "estimated_monthly_sales": self.int_or_none(
                product.get("monthlySold")
            ),
            "raw_data": {
                "source": "keepa_real",
                "title": product.get("title"),
                "brand": product.get("brand"),
                "domain": keepa_domain_for_marketplace(marketplace),
                "stats_current": current,
            },
        }

    async def fetch_market_snapshot(
        self,
        asin: str,
        marketplace: str,
    ) -> dict | None:
        if not asin:
            return None

        metric = await self.fetch_product_metrics(
            asin=asin,
            marketplace=marketplace,
            include_buybox=False,
        )

        if not metric:
            return None

        raw_data = metric.get("raw_data") or {}
        current = raw_data.get("stats_current") or {}

        current_price = self.first_price(
            current,
            [
                "BUY_BOX_SHIPPING",
                "NEW_FBA",
                "NEW",
                "AMAZON",
            ],
        )
        buy_box_price = self.decimal_or_none(
            current.get("BUY_BOX_SHIPPING")
        )

        return {
            "asin": metric["asin"],
            "marketplace": marketplace,
            "current_price": current_price,
            "buy_box_price": buy_box_price,
            "buy_box_exists": buy_box_price is not None,
            "sales_rank": metric["sales_rank"],
            "seller_count": self.int_or_none(
                current.get("COUNT_NEW")
            ),
            "amazon_present": metric["amazon_in_stock"],
            "fba_fee_estimate": None,
            "estimated_monthly_sales": metric["estimated_monthly_sales"],
            "snapshot_source": "keepa_real",
            "raw_data": {
                **raw_data,
                "snapshot_mode": "current_market",
            },
        }

    async def get_token_status(self) -> dict:
        await asyncio.to_thread(self.api.update_status)

        return self.token_status_from_api()

    def token_status_from_api(self) -> dict:
        status = self.api.status

        return {
            "tokens_left": self.api.tokens_left,
            "refill_in": status.refillIn,
            "refill_rate": status.refillRate,
            "timestamp": status.timestamp,
            "time_to_refill_seconds": self.api.time_to_refill,
        }

    @classmethod
    def product_query_token_cost(
        cls,
        include_buybox: bool = False,
    ) -> int:
        return cls.PRODUCT_QUERY_TOKEN_COST + (
            cls.BUYBOX_EXTRA_TOKEN_COST
            if include_buybox
            else 0
        )

    def first_price(
        self,
        values: dict[str, Any],
        keys: list[str],
    ) -> Decimal | None:
        for key in keys:
            price = self.decimal_or_none(
                values.get(key)
            )

            if price is not None:
                return price

        return None

    def decimal_or_none(
        self,
        value,
    ) -> Decimal | None:
        if value is None:
            return None

        try:
            return Decimal(str(value))
        except Exception:
            return None

    def int_or_none(
        self,
        value,
    ) -> int | None:
        if value is None:
            return None

        try:
            return int(value)
        except Exception:
            return None
