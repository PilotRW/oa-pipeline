from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.sql import func

from app.db.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

    created_at = Column(TIMESTAMP, server_default=func.now())