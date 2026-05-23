from fastapi import FastAPI

from app.api.upload import router as upload_router
from app.api.reports import router as reports_router
from app.api import research_queue
from app.api import amazon_matches

app = FastAPI()

app.include_router(upload_router)
app.include_router(reports_router)
app.include_router(research_queue.router)
app.include_router(amazon_matches.router)


@app.get("/")
async def root():
    return {"status": "ok"}