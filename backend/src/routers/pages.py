from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from pathlib import Path
from typing import Optional
import logging

from core.config import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from database.database import get_db
from sqlalchemy.orm import Session
from database.models import User

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Pages"])

# --- CONFIGURAÇÃO DE CAMINHO ---
BASE_DIR: Path = Path(__file__).resolve().parents[3]
STATIC_DIR: Path = BASE_DIR / "frontend" / "static"
ERROR_PAGE_DIR: Path = STATIC_DIR / "errors" 

if not STATIC_DIR.exists():
    logger.critical(f"PASTA STATIC NÃO ENCONTRADA: {STATIC_DIR.resolve()}")

def get_optional_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    """Lê token do Header. Retorna User ou None. Usado só no /"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None: return None
    except JWTError:
        return None
    return db.query(User).filter(User.username == username).first()

def serve_html_page(filename: str) -> FileResponse | HTMLResponse:
    if ".." in filename or filename.startswith("/"):
        logger.warning(f"Tentativa de Path Traversal: {filename}")
        return serve_error_page(404)
    file_path = STATIC_DIR / filename
    if file_path.is_file():
        return FileResponse(file_path)
    logger.error(f"Arquivo HTML não encontrado: {file_path}")
    return serve_error_page(404)

def serve_error_page(status_code: int) -> HTMLResponse:
    error_file = ERROR_PAGE_DIR / f"{status_code}.html"
    if error_file.is_file():
        return HTMLResponse(content=error_file.read_text(encoding="utf-8"), status_code=status_code)
    return HTMLResponse(content=f"<h1>Erro {status_code}</h1>", status_code=status_code)

# --- ROTAS ---

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, user: Optional[User] = Depends(get_optional_user)):
    """Se tiver token no header vai pro /admin, senão fica no login"""
    if user:
        return RedirectResponse(url="/admin", status_code=303)
    return serve_html_page("index.html")

@router.get("/produtos", response_class=HTMLResponse)
async def produtos():
    return serve_html_page("produtos.html")

@router.get("/encomendas", response_class=HTMLResponse)
async def encomendas():
    return serve_html_page("encomendas.html")

@router.get("/quem-somos", response_class=HTMLResponse)
async def quem_somos():
    return serve_html_page("quem-somos.html")

@router.get("/admin", response_class=HTMLResponse)
async def admin_page(): # <-- FIX: Sem Depends. HTML é público
    """Serve o HTML. O JS dentro faz a proteção."""
    return serve_html_page("admin.html")