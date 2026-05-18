from sqlalchemy import Column, BigInteger, Integer, Text, Numeric, TIMESTAMP
from sqlalchemy.sql import func

from app.db.database import Base


class SupplierColumnMapping(Base):
    __tablename__ = "supplier_column_mappings"

    id = Column(BigInteger, primary_key=True)

    supplier_id = Column(Integer, nullable=False)

    source_column = Column(Text, nullable=False)
    target_column = Column(Text, nullable=False)

    confidence = Column(Numeric(5, 2))

    created_at = Column(TIMESTAMP, server_default=func.now())