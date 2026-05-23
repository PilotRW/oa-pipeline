from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class OfferResearchQueue(Base):
    __tablename__ = "offer_research_queue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    supplier_offer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("supplier_offers.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    supplier_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("suppliers.id"),
        nullable=False,
        index=True,
    )

    ean: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="new",
    )

    priority_score: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        Text,
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