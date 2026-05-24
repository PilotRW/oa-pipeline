class MockAmazonMatcher:
    async def match_by_ean(
        self,
        ean: str,
    ) -> dict | None:
        if not ean:
            return None

        if ean.startswith("008838"):
            return {
                "asin": f"MOCK{ean[-6:]}",
                "amazon_title": f"Mock Amazon product for EAN {ean}",
                "amazon_brand": "Makita",
                "match_confidence": 90.0,
            }

        return None