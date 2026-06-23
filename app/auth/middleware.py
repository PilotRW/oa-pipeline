from collections.abc import Awaitable, Callable

from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse, Response

from app.auth.permissions import has_permission, normalize_roles, permissions_for_roles
from app.config.settings import settings

PUBLIC_PREFIXES = (
    "/auth/",
    "/docs",
    "/openapi.json",
    "/redoc",
)
PUBLIC_PATHS = {
    "/",
    "/favicon.ico",
}


def build_dev_user() -> dict:
    roles = normalize_roles(settings.AUTH_DEV_ROLES.split(","))
    if not roles:
        roles = ["owner"]
    return {
        "email": settings.AUTH_DEV_USER,
        "name": settings.AUTH_DEV_USER,
        "roles": roles,
        "permissions": permissions_for_roles(roles),
        "auth_mode": "dev",
    }


def required_permission_for(request: Request) -> str | None:
    path = request.url.path
    method = request.method.upper()

    if method in {"OPTIONS", "HEAD"}:
        return None
    if path.startswith("/config") or path.startswith("/suppliers"):
        return "automation:configure" if method != "GET" else "automation:view"
    if path.startswith("/maintenance/clear-database"):
        return "automation:admin"
    if path.startswith("/maintenance") and method != "GET":
        return "automation:configure"
    if method != "GET":
        return "automation:operate"
    return "automation:view"


def is_public_path(path: str) -> bool:
    return path in PUBLIC_PATHS or any(path.startswith(prefix) for prefix in PUBLIC_PREFIXES)


async def auth_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    if not settings.AUTH_ENABLED:
        request.state.user = build_dev_user()
        return await call_next(request)

    if is_public_path(request.url.path):
        return await call_next(request)

    user = request.session.get("user")
    if not user:
        if request.url.path.startswith("/ui") or "text/html" in request.headers.get("accept", ""):
            return RedirectResponse(url="/auth/login", status_code=303)
        return JSONResponse({"detail": "Authentication required"}, status_code=401)

    request.state.user = user
    permission = required_permission_for(request)
    if permission and not has_permission(user.get("permissions", []), permission):
        return JSONResponse({"detail": f"Missing permission: {permission}"}, status_code=403)

    return await call_next(request)
