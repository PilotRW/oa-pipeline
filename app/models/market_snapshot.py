from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy import JSON, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class MarketSnapshot(Base):
    __tablename__ = "market_snapshots"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    amazon_product_match_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("amazon_product_matches.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    queue_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("offer_research_queue.id"),
        nullable=False,
        index=True,
    )

    supplier_offer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("supplier_offers.id"),
        nullable=False,
        index=True,
    )

    asin: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    marketplace: Mapped[str | None] = mapped_column(String(16), nullable=True)

    current_price: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    buy_box_price: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    buy_box_exists: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    sales_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)

    seller_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    amazon_present: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    fba_fee_estimate: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    estimated_monthly_sales: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    snapshot_source: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    snapshot_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
    )

    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)

    raw_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

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
