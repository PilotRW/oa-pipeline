from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.supplier_offer import SupplierOffer


async def save_supplier_offers(
    session: AsyncSession,
    supplier_id: int,
    df,
) -> int:
    # MVP strategy:
    # each upload fully refreshes offers for this supplier
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
            currency="EUR",
            stock=row.get("stock"),
            raw_data=raw_data,
        )

        offers.append(offer)

    session.add_all(offers)
    await session.flush()

    return len(offers)