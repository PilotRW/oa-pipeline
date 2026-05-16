from fastapi import FastAPI

from app.db.database import engine, Base
from app.models.supplier_offer import SupplierOffer  # <- ВАЖЛИВО

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"status": "ok"}