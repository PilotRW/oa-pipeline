from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    Text,
    Numeric,
    TIMESTAMP,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.database import Base


class SupplierOffer(Base):
    __tablename__ = "supplier_offers"

    id = Column(BigInteger, primary_key=True)

    supplier_id = Column(Integer)

    supplier_sku = Column(Text)

    ean = Column(Text, index=True)

    brand = Column(Text)

    title = Column(Text)

    cost = Column(Numeric(10, 2))

    vat_rate = Column(Numeric(5, 2), nullable=True)

    price_tiers = Column(JSONB, nullable=True)

    supply_channel = Column(
        Text,
        nullable=False,
        default="stock",
        server_default="stock",
        index=True,
    )

    lead_time_min_days = Column(Integer, nullable=True)

    lead_time_max_days = Column(Integer, nullable=True)

    currency = Column(Text)

    stock = Column(Integer)

    raw_data = Column(JSONB)

    imported_at = Column(
        TIMESTAMP,
        server_default=func.now(),
    )
