import asyncio

import keepa

from app.config.settings import settings
from app.services.keepa_client import KeepaConfigurationError
from app.services.marketplace import keepa_domain_for_marketplace


class KeepaAmazonMatcher:
    def __init__(self):
        if (
            not settings.KEEPA_API_KEY
            or settings.KEEPA_API_KEY == "your_keepa_api_key_here"
        ):
            raise KeepaConfigurationError(
                "KEEPA_API_KEY is not configured"
            )

        self.api = keepa.Keepa(
            settings.KEEPA_API_KEY,
            check_key=False,
        )

    async def match_by_ean(
        self,
        ean: str,
        marketplace: str = "DE",
    ) -> dict | None:
        if not ean:
            return None

        products = await asyncio.to_thread(
            self.api.query,
            ean,
            product_code_is_asin=False,
            domain=keepa_domain_for_marketplace(marketplace),
            stats=1,
            history=False,
            progress_bar=False,
        )

        if not products:
            return None

        product = products[0]

        asin = product.get("asin")
        title = product.get("title")
        brand = product.get("brand")

        if not asin:
            return None

        return {
            "asin": asin,
            "amazon_title": title,
            "amazon_brand": brand,
            "match_confidence": 95.0,
        }
