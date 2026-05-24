from app.config.settings import settings
from app.services.amazon_matchers.keepa_matcher import KeepaAmazonMatcher
from app.services.amazon_matchers.mock_matcher import MockAmazonMatcher


def get_amazon_matcher():
    if settings.USE_KEEPA_REAL_API:
        return KeepaAmazonMatcher()

    return MockAmazonMatcher()