from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.supplier import Supplier
from app.models.supplier_offer import SupplierOffer
from app.services.procurement_comparison_service import (
    compare_product_offers,
    ean_lookup_variants,
    parse_product_list,
)


router = APIRouter(prefix="/procurement", tags=["procurement"])


class ProcurementCompareRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    products: str = Field(min_length=1, max_length=100_000)
    target_currency: str = Field(default="EUR", min_length=3, max_length=3)
    purchase_quantity: int = Field(default=1, ge=1, le=1_000_000)
    include_hidden_suppliers: bool = False

    @field_validator("target_currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        if not value.isalpha():
            raise ValueError("Currency must be a three-letter code")
        return value.upper()


@router.post("/compare")
async def compare_procurement_prices(
    payload: ProcurementCompareRequest,
    db: AsyncSession = Depends(get_db),
):
    products, invalid_lines = parse_product_list(payload.products)
    requested_eans = sorted({
        variant
        for item in products
        for variant in ean_lookup_variants(item["ean"])
    })

    candidates: list[dict] = []
    if requested_eans:
        query = (
            select(SupplierOffer, Supplier)
            .join(Supplier, Supplier.id == SupplierOffer.supplier_id)
            .where(SupplierOffer.ean.in_(requested_eans))
            .where(SupplierOffer.cost.is_not(None))
        )
        if not payload.include_hidden_suppliers:
            query = query.where(Supplier.is_visible.is_(True))

        rows = (await db.execute(query)).all()
        candidates = [
            {
                "ean": offer.ean,
                "offer_id": offer.id,
                "supplier_id": supplier.id,
                "supplier": supplier.name,
                "supplier_sku": offer.supplier_sku,
                "title": offer.title,
                "brand": offer.brand,
                "cost": offer.cost,
                "currency": offer.currency,
                "price_tiers": offer.price_tiers,
                "raw_data": offer.raw_data,
                "source_file": (
                    offer.raw_data.get("source_file")
                    if isinstance(offer.raw_data, dict)
                    else None
                ),
                "stock": offer.stock,
                "supply_channel": offer.supply_channel,
                "lead_time_min_days": offer.lead_time_min_days,
                "lead_time_max_days": offer.lead_time_max_days,
                "imported_at": offer.imported_at,
            }
            for offer, supplier in rows
        ]

    results = compare_product_offers(
        products,
        candidates,
        payload.target_currency,
        payload.purchase_quantity,
    )
    matched = sum(item["status"] == "matched" for item in results)
    located = sum(item["offers_found"] > 0 for item in results)
    offers_found = sum(item["offers_found"] for item in results)
    not_found = sum(item["status"] == "not_found" for item in results)

    return {
        "target_currency": payload.target_currency,
        "purchase_quantity": payload.purchase_quantity,
        "requested": len(products),
        "located": located,
        "offers_found": offers_found,
        "matched": matched,
        "needs_configuration": located - matched,
        "not_found": not_found,
        "unmatched": len(products) - matched,
        "invalid_lines": invalid_lines,
        "results": results,
    }
