from sqlalchemy import Column, BigInteger, Integer, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.database import Base


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id = Column(BigInteger, primary_key=True)

    supplier_id = Column(Integer, nullable=False)
    filename = Column(Text, nullable=False)

    status = Column(Text, nullable=False, default="completed")

    rows_total = Column(Integer, default=0)
    rows_valid = Column(Integer, default=0)
    rows_failed = Column(Integer, default=0)

    normalization_report = Column(JSONB)

    created_at = Column(TIMESTAMP, server_default=func.now())