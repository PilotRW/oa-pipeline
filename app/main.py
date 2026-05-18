from fastapi import FastAPI

from app.api.upload import router as upload_router
from app.api.reports import router as reports_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(reports_router)


@app.get("/")
async def root():
    return {"status": "ok"}