from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class DealCandidate(Base):
    __tablename__ = "deal_candidates"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    supplier_offer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("supplier_offers.id"),
        nullable=False,
        index=True,
    )

    asin: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    supplier_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    amazon_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    estimated_fees: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    estimated_profit: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    roi_percent: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    sales_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)

    estimated_monthly_sales: Mapped[int | None] = mapped_column(Integer, nullable=True)

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
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