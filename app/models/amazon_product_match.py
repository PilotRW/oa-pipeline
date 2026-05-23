from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AmazonProductMatch(Base):
    __tablename__ = "amazon_product_matches"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    queue_id: Mapped[int] = mapped_column(
        ForeignKey("offer_research_queue.id"),
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

    ean: Mapped[str] = mapped_column(Text, nullable=False, index=True)

    asin: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)

    match_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
    )

    match_confidence: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    amazon_title: Mapped[str | None] = mapped_column(Text, nullable=True)

    amazon_brand: Mapped[str | None] = mapped_column(Text, nullable=True)

    matched_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )