from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ResearchRule(Base):
    __tablename__ = "research_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    min_priority_score: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=80,
    )

    min_stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    low_stock_threshold: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    medium_stock_threshold: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=3,
    )

    high_stock_threshold: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=20,
    )

    preferred_cost_min: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=20,
    )

    preferred_cost_max: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=300,
    )

    medium_cost_max: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=1000,
    )

    min_cost: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=5,
    )

    min_roi_percent: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=20,
    )

    min_profit: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    max_sales_rank: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    min_monthly_sales: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    exclude_amazon_in_stock: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    # -------- Scoring weights --------

    score_stock_high: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=30,
    )

    score_stock_medium: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=20,
    )

    score_stock_low: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=10,
    )

    score_stock_very_low: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=-20,
    )

    score_cost_preferred: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=30,
    )

    score_cost_medium: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=15,
    )

    score_cost_high: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=-10,
    )

    score_cost_low: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=-20,
    )

    score_brand_present: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=15,
    )

    score_title_present: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=15,
    )

    score_ean_present: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=10,
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