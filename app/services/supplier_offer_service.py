from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.amazon_product_match import AmazonProductMatch
from app.models.deal_candidate import DealCandidate
from app.models.offer_research_queue import OfferResearchQueue
from app.models.supplier_offer import SupplierOffer


async def save_supplier_offers(
    session: AsyncSession,
    supplier_id: int,
    df,
    currency: str,
) -> int:
    # MVP strategy:
    # each upload fully refreshes offers for this supplier
    supplier_offer_ids = select(SupplierOffer.id).where(
        SupplierOffer.supplier_id == supplier_id
    )
    queue_ids = select(OfferResearchQueue.id).where(
        OfferResearchQueue.supplier_id == supplier_id
    )

    await session.execute(
        delete(DealCandidate).where(
            DealCandidate.supplier_offer_id.in_(
                supplier_offer_ids
            )
        )
    )

    await session.execute(
        delete(AmazonProductMatch).where(
            AmazonProductMatch.queue_id.in_(
                queue_ids
            )
        )
    )

    await session.execute(
        delete(OfferResearchQueue).where(
            OfferResearchQueue.supplier_id == supplier_id
        )
    )

    await session.execute(
        delete(SupplierOffer).where(
            SupplierOffer.supplier_id == supplier_id
        )
    )

    offers = []

    for _, row in df.iterrows():
        raw_data = row.to_dict()

        offer = SupplierOffer(
            supplier_id=supplier_id,
            supplier_sku=row.get("supplier_sku"),
            ean=row.get("ean"),
            brand=row.get("brand"),
            title=row.get("title"),
            cost=row.get("price"),
            currency=currency,
            stock=row.get("stock"),
            raw_data=raw_data,
        )

        offers.append(offer)

    session.add_all(offers)
    await session.flush()

    return len(offers)
