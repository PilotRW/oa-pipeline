from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class PipelineSetting(Base):
    __tablename__ = "pipeline_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    use_real_keepa: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    default_batch_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=20,
    )

    default_marketplace: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="DE",
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