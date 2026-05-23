from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, JSON, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class KeepaProductMetric(Base):
    __tablename__ = "keepa_product_metrics"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    asin: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True,
        index=True,
    )

    buy_box_price: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    currency: Mapped[str | None] = mapped_column(
        String(8),
        nullable=True,
    )

    sales_rank: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    amazon_in_stock: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    estimated_monthly_sales: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    data_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
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