import asyncio
from decimal import Decimal
from typing import Any

import keepa

from app.config.settings import settings
from app.services.marketplace import keepa_domain_for_marketplace


class KeepaConfigurationError(ValueError):
    pass


class KeepaMetricsClient:
    def __init__(
        self,
        api_key: str | None = None,
    ):
        self.api_key = api_key or settings.KEEPA_API_KEY

        if (
            not self.api_key
            or self.api_key == "your_keepa_api_key_here"
        ):
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
    ) -> dict | None:
        if not asin:
            return None

        products = await asyncio.to_thread(
            self.api.query,
            asin,
            stats=30,
            domain=keepa_domain_for_marketplace(marketplace),
            history=False,
            product_code_is_asin=True,
            progress_bar=False,
            buybox=True,
        )

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
