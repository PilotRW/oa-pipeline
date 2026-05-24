from app.config.settings import settings
from app.services.amazon_matchers.keepa_matcher import KeepaAmazonMatcher
from app.services.amazon_matchers.mock_matcher import MockAmazonMatcher


def get_amazon_matcher(
    use_real_keepa: bool | None = None,
):
    real_keepa_enabled = (
        settings.USE_KEEPA_REAL_API
        if use_real_keepa is None
        else use_real_keepa
    )

    if real_keepa_enabled:
        return KeepaAmazonMatcher()

    return MockAmazonMatcher()
