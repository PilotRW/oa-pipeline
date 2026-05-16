from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from app.config.settings import settings

engine = create_async_engine(settings.DATABASE_URL)
Base = declarative_base()