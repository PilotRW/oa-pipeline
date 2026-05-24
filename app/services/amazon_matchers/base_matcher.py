from typing import Protocol


class AmazonMatchResult(dict):
    pass


class BaseAmazonMatcher(Protocol):
    async def match_by_ean(
        self,
        ean: str,
    ) -> dict | None:
        ...