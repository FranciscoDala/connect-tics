from contextlib import asynccontextmanager
from pathlib import Path
import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

from database.database import engine, Base, SessionLocal
from database.models import User
from core.security import hash_password
from api import auth
from routers import pages, admin, posts, categories

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================================================================
# CORRIGIDO V32: APONTA PRA RAIZ/FRONTEND/STATIC
# ===================================================================
BACKEND_DIR = Path(__file__).resolve().parent.parent  # /src/backend/src -> /src/backend
PROJECT_ROOT = BACKEND_DIR.parent                     # /src/backend -> /src
STATIC_DIR = PROJECT_ROOT / "frontend" / "static"     # /src/frontend/static  <-- AQUI ESTÁ O TEU CSS/JS/IMG
UPLOADS_DIR = STATIC_DIR / "assets" / "img" / "uploads" 

if not STATIC_DIR.exists():
    raise RuntimeError(f"❌ ERRO FATAL: Pasta não existe: {STATIC_DIR.resolve()}")
# ===================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Criando tabelas e seed admin...")
    Base.metadata.create_all(bind=engine, checkfirst=True) # <-- SÓ MUDOU AQUI
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"📁 PASTA UPLOADS GARANTIDA: {UPLOADS_DIR.resolve()}")
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            db.add(User(username="admin", hashed_password=hash_password("admin123")))
            db.commit()
            logger.info("✅ Admin seed criado: admin / admin123")
        from database.models import Category
        if not db.query(Category).filter(Category.name == "Destaques").first():
            db.add(Category(name="Destaques"))
            db.commit()
            logger.info("✅ Seed categoria: Destaques")
    finally:
        db.close()
    yield

app = FastAPI(title="Connect-Tics API", version="1.0.0", lifespan=lifespan, docs_url="/docs", redoc_url=None)

class NoCacheHTMLMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.url.path.endswith(("/", "/index", "/admin")) or "." not in request.url.path.split("/")[-1]:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response
app.add_middleware(NoCacheHTMLMiddleware)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(posts.router, prefix="/admin")
app.include_router(categories.router, prefix="/admin")
app.include_router(pages.router)

logger.info(f"====================================")
logger.info(f"📁 PROJECT_ROOT: {PROJECT_ROOT.resolve()}")
logger.info(f"📁 PASTA STATIC: {STATIC_DIR.resolve()}")
logger.info(f"📁 PASTA UPLOADS: {UPLOADS_DIR.resolve()}")
logger.info(f"📁 STATIC EXISTE? {STATIC_DIR.exists()}")
logger.info(f"📁 UPLOADS EXISTE? {UPLOADS_DIR.exists()}")
logger.info(f"====================================")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str):
    if full_path.startswith(("api/", "admin/", "docs", "openapi.json")):
        return JSONResponse(status_code=404, content={"detail": "Not Found"})
    file_path = STATIC_DIR / full_path
    if "." in full_path and not file_path.exists():
        return JSONResponse(status_code=404, content={"detail": "Not Found"})
    return FileResponse(STATIC_DIR / "index.html")