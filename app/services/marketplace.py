def currency_for_marketplace(
    marketplace: str,
) -> str:
    currencies = {
        "DE": "EUR",
        "FR": "EUR",
        "IT": "EUR",
        "ES": "EUR",
        "NL": "EUR",
        "BE": "EUR",
        "UK": "GBP",
        "US": "USD",
    }

    return currencies.get(marketplace.upper(), "EUR")


def keepa_domain_for_marketplace(
    marketplace: str,
) -> str:
    domains = {
        "UK": "GB",
    }

    normalized = marketplace.upper()

    return domains.get(normalized, normalized)
