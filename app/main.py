"""Quizocracy, the product: a separate service from the family app (hw.quizocracy.com)."""
import asyncio
from contextlib import asynccontextmanager
from urllib.parse import urlparse

from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import config, errors, levels
from .config import BASE_DIR
from .db import db, ensure_indexes
from .deps import Redirect, load
from .routes import auth, child, extras, parent, team
from .web import page


@asynccontextmanager
async def lifespan(app):
    await ensure_indexes()
    await levels.fix_all()          # children set up with one "working at" for every subject (before Nov 2026)
    count = asyncio.create_task(errors.daily_count())
    yield
    count.cancel()


app = FastAPI(title="Quizocracy", lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
for r in (auth.router, parent.router, child.router, team.router, extras.router):
    app.include_router(r)


@app.exception_handler(Redirect)
async def _redirect(request: Request, exc: Redirect):
    if request.url.path.startswith("/api/"):
        return JSONResponse({"ok": False, "error": "auth"}, status_code=401)
    return RedirectResponse(exc.url, 303)


# Any other exception is a 500: a friendly page, a log line and a throttled email to the operator (app/errors.py).
app.add_exception_handler(Exception, errors.handler)


@app.exception_handler(StarletteHTTPException)
async def _http_error(request: Request, exc: StarletteHTTPException):
    """An unknown address (or a page that isn't this family's) gets a friendly page with a way back; /api/ keeps
    its JSON 404 and /static/ its plain one, and every other status is handled as before."""
    path = request.url.path
    if exc.status_code != 404 or path.startswith(("/api/", "/static/")):
        return await http_exception_handler(request, exc)
    try:
        ctx = await load(request)
    except Exception:  # noqa: BLE001 - the page must show even when the session can't be read
        ctx = None
    return page(request, "not_found.html", ctx, status_code=404)


# ---- For search engines: the public pages may be listed; the family and team areas may not ----
PUBLIC_PAGES = ("/", "/signup", "/login", "/help", "/privacy", "/terms")
PRIVATE_AREAS = ("/home", "/me", "/learn", "/board", "/children/", "/settings", "/account/", "/team/", "/api/",
                 "/verify", "/reset", "/invite", "/handover", "/parent-unlock", "/not-allowed", "/unsubscribe",
                 "/waitlist", "/logout")


@app.get("/robots.txt")
async def robots():
    lines = ["User-agent: *"] + [f"Disallow: {p}" for p in PRIVATE_AREAS] + [f"Allow: {p}" for p in PUBLIC_PAGES]
    return PlainTextResponse("\n".join(lines + ["", f"Sitemap: {config.PUBLIC_URL}/sitemap.xml", ""]))


@app.get("/sitemap.xml")
async def sitemap():
    urls = "".join(f"  <url><loc>{config.PUBLIC_URL}{p}</loc></url>\n" for p in PUBLIC_PAGES)
    return Response('<?xml version="1.0" encoding="UTF-8"?>\n'
                    f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n',
                    media_type="application/xml")


SAFE = {"GET", "HEAD", "OPTIONS"}


@app.middleware("http")
async def guard(request: Request, call_next):
    # Cross-site requests may not change anything (cookies are SameSite=Lax as a second layer).
    if request.method not in SAFE:
        origin = request.headers.get("origin") or request.headers.get("referer")
        if origin:
            # "Origin: null" (sandboxed frames, data: pages, some redirects) has no host: it is refused too.
            host = urlparse(origin).netloc
            if not host or (host != request.headers.get("host") and host != urlparse(config.PUBLIC_URL).netloc):
                return PlainTextResponse("cross-site request refused", status_code=403)
    resp = await call_next(request)
    if resp.headers.get("content-type", "").startswith("text/html") or request.url.path.startswith("/api/"):
        resp.headers["Cache-Control"] = "no-store"          # WebViews must never show stale pages or answers
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("Referrer-Policy", "same-origin")
    resp.headers.setdefault("X-Frame-Options", "DENY")
    if request.url.path.startswith("/team"):
        resp.headers["X-Robots-Tag"] = "noindex, nofollow"     # private board links stay out of search engines
    return resp


@app.get("/")
async def landing(request: Request):
    ctx = await load(request)
    if ctx and ctx.account.get("verified_at"):
        return RedirectResponse("/me" if ctx.child else ("/learn" if ctx.locked else "/home"), 303)
    return page(request, "landing.html", ctx)


@app.get("/pricing")
async def pricing():
    return RedirectResponse("/", 303)          # no prices in this version


@app.get("/privacy")
async def privacy(request: Request):
    return page(request, "privacy.html", await load(request))


@app.get("/terms")
async def terms(request: Request):
    return page(request, "terms.html", await load(request))


@app.get("/healthz")
async def healthz():
    """For the uptime check (scripts/uptime_check.py): 503 when the database does not answer a ping within 2 s."""
    try:
        await asyncio.wait_for(db.command("ping"), 2)
    except Exception:  # noqa: BLE001 - any failure to ping means the database is down for us
        return JSONResponse({"ok": False, "db": "down"}, status_code=503)
    return {"ok": True, "db": "ok"}
