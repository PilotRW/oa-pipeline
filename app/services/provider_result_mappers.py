from datetime import datetime, timezone


def apply_market_snapshot_result(snapshot, result: dict) -> None:
    fields = (
        "marketplace",
        "current_price",
        "buy_box_price",
        "buy_box_exists",
        "sales_rank",
        "seller_count",
        "amazon_present",
        "fba_fee_estimate",
        "estimated_monthly_sales",
        "snapshot_source",
        "raw_data",
    )
    for field in fields:
        setattr(snapshot, field, result.get(field))
    snapshot.error_message = None


def apply_keepa_metric_result(
    metric,
    result: dict,
    fallback_currency: str,
) -> None:
    metric.buy_box_price = result.get("buy_box_price")
    metric.currency = result.get("currency") or fallback_currency
    metric.sales_rank = result.get("sales_rank")
    metric.amazon_in_stock = result.get("amazon_in_stock")
    metric.estimated_monthly_sales = result.get("estimated_monthly_sales")
    metric.data_status = "completed"
    metric.raw_data = result.get("raw_data")


def apply_presence_result(
    check,
    *,
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


def mock_amazon_presence(asin: str) -> bool:
    return sum(ord(character) for character in asin or "") % 3 == 0
