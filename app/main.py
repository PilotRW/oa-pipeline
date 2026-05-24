from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.upload import router as upload_router
from app.api.reports import router as reports_router
from app.api import research_queue
from app.api import amazon_matches
from app.api import keepa
from app.api import deals
from app.api import pipeline
from app.api import config

app = FastAPI()

app.mount("/ui", StaticFiles(directory="app/static", html=True), name="ui")

app.include_router(upload_router)
app.include_router(reports_router)
app.include_router(research_queue.router)
app.include_router(amazon_matches.router)
app.include_router(keepa.router)
app.include_router(deals.router)
app.include_router(pipeline.router)
app.include_router(config.router)


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/dashboard", include_in_schema=False)
async def dashboard():
    return RedirectResponse(url="/ui/")
