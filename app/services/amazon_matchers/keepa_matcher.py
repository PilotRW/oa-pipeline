import asyncio

import keepa

from app.config.settings import settings


class KeepaAmazonMatcher:
    def __init__(self):
        if not settings.KEEPA_API_KEY:
            raise ValueError("KEEPA_API_KEY is not configured")

        self.api = keepa.Keepa(settings.KEEPA_API_KEY)

    async def match_by_ean(
        self,
        ean: str,
    ) -> dict | None:
        if not ean:
            return None

        products = await asyncio.to_thread(
            self.api.query,
            ean,
            product_code_is_asin=False,
            stats=1,
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