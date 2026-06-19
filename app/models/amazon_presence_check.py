from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AmazonPresenceCheck(Base):
    __tablename__ = "amazon_presence_checks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    amazon_product_match_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("amazon_product_matches.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    supplier_offer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("supplier_offers.id"),
        nullable=False,
        index=True,
    )

    asin: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True,
    )

    marketplace: Mapped[str | None] = mapped_column(
        String(8),
        nullable=True,
    )

    amazon_present: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    presence_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
        index=True,
    )

    data_source: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    checked_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    raw_data: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
