from sqlalchemy import BigInteger, Boolean, Column, Integer, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    is_visible = Column(Boolean, nullable=False, default=True)
    price_url = Column(Text, nullable=True)
    import_filter_profile = Column(JSONB, nullable=True)
    price_etag = Column(Text, nullable=True)
    price_last_modified = Column(Text, nullable=True)
    price_content_length = Column(BigInteger, nullable=True)
    price_file_hash = Column(Text, nullable=True)
    price_data_hash = Column(Text, nullable=True)
    price_last_filename = Column(Text, nullable=True)
    price_update_status = Column(Text, nullable=True)
    price_last_checked_at = Column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )
    price_last_downloaded_at = Column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )
    price_last_changed_at = Column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )

    created_at = Column(TIMESTAMP, server_default=func.now())
