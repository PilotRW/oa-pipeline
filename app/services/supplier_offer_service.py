from datetime import date, datetime
from decimal import Decimal, InvalidOperation
import math

import pandas as pd

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.amazon_product_match import AmazonProductMatch
from app.models.amazon_presence_check import AmazonPresenceCheck
from app.models.deal_candidate import DealCandidate
from app.models.market_snapshot import MarketSnapshot
from app.models.offer_research_queue import OfferResearchQueue
from app.models.supplier_offer import SupplierOffer
from app.ingestion.cleaners import clean_stock
from app.services.price_tier_service import extract_price_tiers


def optional_decimal(value):
    if value is None or value == "":
        return None

    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


def json_safe_value(value):
    if isinstance(value, dict):
        return {
            str(key): json_safe_value(item)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple, set)):
        return [json_safe_value(item) for item in value]
    if value is None or value is pd.NA:
        return None
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if hasattr(value, "item") and callable(value.item):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


async def delete_supplier_catalog_data(
    session: AsyncSession,
    supplier_id: int,
    supply_channels: set[str] | None = None,
) -> dict[str, int]:
    supplier_offer_ids = select(SupplierOffer.id).where(
        SupplierOffer.supplier_id == supplier_id
    )
    if supply_channels:
        supplier_offer_ids = supplier_offer_ids.where(
            SupplierOffer.supply_channel.in_(supply_channels)
        )
    deleted = {}
    statements = [
        (
            "amazon_presence_checks",
            delete(AmazonPresenceCheck).where(
                AmazonPresenceCheck.supplier_offer_id.in_(
                    supplier_offer_ids
                )
            ),
        ),
        (
            "market_snapshots",
            delete(MarketSnapshot).where(
                MarketSnapshot.supplier_offer_id.in_(supplier_offer_ids)
            ),
        ),
        (
            "deal_candidates",
            delete(DealCandidate).where(
                DealCandidate.supplier_offer_id.in_(supplier_offer_ids)
            ),
        ),
        (
            "amazon_product_matches",
            delete(AmazonProductMatch).where(
                AmazonProductMatch.supplier_offer_id.in_(supplier_offer_ids)
            ),
        ),
        (
            "offer_research_queue",
            delete(OfferResearchQueue).where(
                OfferResearchQueue.supplier_offer_id.in_(
                    supplier_offer_ids
                )
            ),
        ),
        (
            "supplier_offers",
            delete(SupplierOffer).where(
                SupplierOffer.id.in_(supplier_offer_ids)
            ),
        ),
    ]
    for name, statement in statements:
        result = await session.execute(statement)
        deleted[name] = max(int(result.rowcount or 0), 0)

    return deleted


async def save_supplier_offers(
    session: AsyncSession,
    supplier_id: int,
    df,
    currency: str,
) -> int:
    channels = {
        str(value).strip().lower()
        for value in df.get("supply_channel", [])
        if pd.notna(value) and str(value).strip()
    }
    if not channels:
        channels = {"stock"}
    # Refresh only imported supply channels; preserve the supplier's other feeds.
    await delete_supplier_catalog_data(
        session,
        supplier_id,
        supply_channels=channels,
    )

    offers = []

    for _, row in df.iterrows():
        raw_data = json_safe_value(row.to_dict())

        offer = SupplierOffer(
            supplier_id=supplier_id,
            supplier_sku=row.get("supplier_sku"),
            ean=row.get("ean"),
            brand=row.get("brand"),
            title=row.get("title"),
            cost=optional_decimal(row.get("price")),
            vat_rate=optional_decimal(row.get("vat_rate")),
            price_tiers=extract_price_tiers(raw_data, row.get("price")),
            supply_channel=str(
                row.get("supply_channel") or "stock"
            ).strip().lower(),
            lead_time_min_days=clean_stock(
                row.get("lead_time_min_days")
            ),
            lead_time_max_days=clean_stock(
                row.get("lead_time_max_days")
            ),
            currency=str(row.get("currency") or currency).strip().upper(),
            stock=clean_stock(row.get("stock")),
            raw_data=raw_data,
        )

        offers.append(offer)

    session.add_all(offers)
    await session.flush()

    return len(offers)
