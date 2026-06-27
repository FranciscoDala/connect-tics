import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# ===== 1. FIX IMPORTS: Adiciona a pasta src no Python Path =====
SRC_DIR = Path(__file__).resolve().parent
sys.path.append(str(SRC_DIR))

from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from jose import jwt, JWTError
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# ===== 2. IMPORTS DO TEU PROJETO - CORRIGIDO =====
from database.database import engine, get_db, Base, SessionLocal # <-- ADICIONEI SessionLocal AQUI
from database.models import User
from api.auth import verify_password, hash_password

# ===== CARREGAR.ENV =====
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "troca-esta-chave-em-prod")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

# ===== INICIALIZAÇÃO DA API =====
app = FastAPI(
    title="Connect-Tics API",
    description="API do site Connect-Tics. Serve o frontend e endpoints.",
    version="0.3.1"
)

# ===== MIDDLEWARE SESSÃO + CORS =====
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://azulula-mbugue.vercel.app",
        "http://localhost:5500",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 3. CRIAR TABELAS NO STARTUP - SEM temp_engine =====
@app.on_event("startup")
def startup_db():
    DATABASE_URL = os.getenv("DATABASE_URL")
    print(f">>> 1. STARTUP INICIADO")
    print(f">>> 2. DATABASE_URL = {DATABASE_URL[:40]}..." if DATABASE_URL else ">>> 2. DATABASE_URL = VAZIA")

    try:
        print(">>> 3. TENTANDO CRIAR TABELAS COM O ENGINE DO DATABASE.PY...")
        Base.metadata.create_all(bind=engine) # <-- USA O ENGINE DO database.py AGORA
        print(">>> 4. TABELAS CRIADAS OK")

        db: Session = SessionLocal() # <-- USA A MESMA SESSAO DAS ROTAS
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            new_admin = User(username="admin", hashed_password=hash_password("admin123"))
            db.add(new_admin)
            db.commit()
            print(">>> 5. User admin criado: admin / admin123")
        else:
            print(">>> 5. Admin já existe")
        db.close()
        print(">>> 6. SUCESSO TOTAL NO BANCO")

    except Exception as e:
        print(f">>> ERRO FATAL NO STARTUP: {type(e).__name__} - {e}")

# ===== CAMINHOS DE PASTAS =====
BASE_DIR = Path(__file__).resolve().parents[2]
STATIC_DIR = BASE_DIR / "frontend" / "static"

print(f">>> BASE_DIR: {BASE_DIR}")
print(f">>> STATIC_DIR: {STATIC_DIR}")
print(f">>> PASTA EXISTE? {STATIC_DIR.exists()}")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ===== DB FALSO DE POSTS =====
posts_db = [
    {"id": 1, "titulo": "Bem-vindo ao Connect-Tics", "conteudo": "Este é o primeiro post."}
]

# ===== FUNÇÕES AUTH =====
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.session.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# ===== FUNÇÃO AUXILIAR =====
def get_html_file(filename: str):
    file_path = os.path.join(STATIC_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse(
            status_code=404,
            content={"error": f"Arquivo não encontrado: {filename}", "path": file_path}
        )
    return FileResponse(file_path)

# ===== ROTAS QUE DEVOLVEM HTML =====
@app.get("/", tags=["Pages"])
async def home(request: Request):
    return get_html_file("index.html")

@app.get("/produtos", tags=["Pages"])
async def produtos():
    return get_html_file("produtos.html")

@app.get("/encomendas", tags=["Pages"])
async def encomendas():
    return get_html_file("encomendas.html")

@app.get("/quem-somos", tags=["Pages"])
async def quem_somos():
    return get_html_file("quem-somos.html")

# ===== ROTAS ADMIN - LOGIN/LOGOUT/PAINEL =====
@app.post("/login", tags=["Auth"])
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password): # type: ignore
        return JSONResponse(status_code=401, content={"detail": "Usuário ou senha inválidos"})

    access_token = create_access_token(data={"sub": user.username})
    request.session["access_token"] = access_token

    return JSONResponse(status_code=200, content={"success": True, "redirect": "/admin"})

@app.get("/admin", tags=["Admin"])
async def admin_page(user: str = Depends(get_current_user)):
    return get_html_file("admin.html")

@app.get("/logout", tags=["Auth"])
async def logout(request: Request):
    request.session.pop("access_token", None)
    return RedirectResponse(url="/", status_code=303)

@app.post("/admin/criar", tags=["Admin"])
async def criar_post(
    titulo: str = Form(...),
    conteudo: str = Form(...),
    user: str = Depends(get_current_user)
):
    novo_id = len(posts_db) + 1
    posts_db.append({"id": novo_id, "titulo": titulo, "conteudo": conteudo})
    return RedirectResponse(url="/admin", status_code=303)