from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
try:
    from starlette.middleware.sessions import SessionMiddleware
except ModuleNotFoundError:
    SessionMiddleware = None

from app.api.upload import router as upload_router
from app.api.reports import router as reports_router
from app.api import research_queue
from app.api import amazon_matches
from app.api import amazon_presence
from app.api import keepa
from app.api import deals
from app.api import pipeline
from app.api import config
from app.api import suppliers
from app.api import maintenance
from app.auth.middleware import auth_middleware
from app.auth.routes import router as auth_router
from app.config.settings import settings

app = FastAPI()

app.middleware("http")(auth_middleware)
if SessionMiddleware is None:
    if settings.AUTH_ENABLED:
        raise RuntimeError("AUTH_ENABLED=true requires the itsdangerous package.")
else:
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.AUTH_SESSION_SECRET,
        same_site="lax",
        https_only=settings.AUTH_ENABLED,
    )

app.mount("/ui", StaticFiles(directory="app/static", html=True), name="ui")

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(reports_router)
app.include_router(research_queue.router)
app.include_router(amazon_matches.router)
app.include_router(amazon_presence.router)
app.include_router(keepa.router)
app.include_router(deals.router)
app.include_router(pipeline.router)
app.include_router(config.router)
app.include_router(suppliers.router)
app.include_router(maintenance.router)


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/dashboard", include_in_schema=False)
async def dashboard():
    return RedirectResponse(url="/ui/")
