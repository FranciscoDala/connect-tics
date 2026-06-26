import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# ===== 1. FIX IMPORTS: Adiciona a pasta src no Python Path =====
# __file__ = A:\site_web\backend\src\main.py
#.parent = A:\site_web\backend\src
SRC_DIR = Path(__file__).resolve().parent
sys.path.append(str(SRC_DIR)) # Adiciona 'src' pro Python achar 'database' e 'api'

from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from jose import jwt, JWTError
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# ===== 2. IMPORTS DO TEU PROJETO =====
from database.database import engine, get_db, Base
from database.models import User
from api.auth import verify_password, hash_password

# ===== CARREGAR.ENV =====
load_dotenv() # Carrega as variáveis do ficheiro.env
SECRET_KEY = os.getenv("SECRET_KEY", "troca-esta-chave-em-prod") # Chave pra assinar o JWT
ALGORITHM = os.getenv("ALGORITHM", "HS256") # Algoritmo do JWT
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120")) # 2 horas

# ===== INICIALIZAÇÃO DA API =====
app = FastAPI(
    title="Connect-Tics API",
    description="API do site Connect-Tics. Serve o frontend e endpoints.",
    version="0.3.0" 
)

# ===== MIDDLEWARE SESSÃO + CORS =====
# SessionMiddleware: Cria o 'request.session' pra guardar o token JWT do user logado
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY) 
# CORSMiddleware: Libera o frontend Vercel/Localhost de acessar esta API
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

# ===== 3. CRIAR TABELAS NO STARTUP =====
# Roda 1 vez quando o server inicia
@app.on_event("startup")
def startup_db():
    Base.metadata.create_all(bind=engine) # Cria todas as tabelas do models.py se não existirem
    db: Session = next(get_db()) # Abre uma sessão com o BD só pra criar o admin
    admin = db.query(User).filter(User.username == "admin").first() # Procura se admin já existe
    if not admin: # Se não existe, cria
        new_admin = User(
            username="admin", 
            hashed_password=hash_password("admin123") # Senha já vem encriptada
        )
        db.add(new_admin)
        db.commit() # Salva no BD
        print(">>> User admin criado: admin / admin123")
    db.close() # Fecha a sessão

# ===== CAMINHOS DE PASTAS =====
#.parents[2] = Sobe 2 níveis: src -> backend -> site_web
BASE_DIR = Path(__file__).resolve().parents[2] 
STATIC_DIR = BASE_DIR / "frontend" / "static" # Pasta onde estão os.html

print(f">>> BASE_DIR: {BASE_DIR}")
print(f">>> STATIC_DIR: {STATIC_DIR}")
print(f">>> PASTA EXISTE? {STATIC_DIR.exists()}")

# Monta a pasta /static pra servir CSS, JS, Imagens
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ===== DB FALSO DE POSTS =====
# TODO: Trocar isso por tabela 'posts' no SQLite depois
posts_db = [
    {"id": 1, "titulo": "Bem-vindo ao Connect-Tics", "conteudo": "Este é o primeiro post."}
]

# ===== FUNÇÕES AUTH =====
def create_access_token(data: dict):
    """Cria o token JWT com tempo de expiração"""
    to_encode = data.copy() # Pega {"sub": "admin"}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # Define expira em 2h
    to_encode.update({"exp": expire}) # Adiciona 'exp' no token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # Gera a string do token

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Dependência de proteção. Roda em toda rota @Depends(get_current_user)"""
    token = request.session.get("access_token") # Pega o token que guardamos no login
    if not token: # Se não tem token = não logou
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # Decodifica e valida o token
        username: str = payload.get("sub") # Pega o username de dentro do token
        user = db.query(User).filter(User.username == username).first() # Confere se user ainda existe no BD
        if not user:
            raise HTTPException(status_code=401, detail="Usuário inválido")
        return username # Se tá tudo ok, devolve o username
    except JWTError: # Se token expirado ou inválido
        raise HTTPException(status_code=401, detail="Token inválido")

# ===== FUNÇÃO AUXILIAR =====
def get_html_file(filename: str):
    """Função pra não repetir código. Serve qualquer.html da pasta static"""
    file_path = os.path.join(STATIC_DIR, filename)
    if not os.path.exists(file_path): # Se o ficheiro não existe
        return JSONResponse(
            status_code=404, 
            content={"error": f"Arquivo não encontrado: {filename}", "path": file_path}
        )
    return FileResponse(file_path) # Devolve o.html

# ===== ROTAS QUE DEVOLVEM HTML =====

@app.get("/", tags=["Pages"])
async def home(request: Request): 
    """Rota da página inicial. Serve /frontend/static/index.html"""
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
    username: str = Form(...), # Pega do form: <input name="username">
    password: str = Form(...), # Pega do form: <input name="password">
    db: Session = Depends(get_db) # Abre conexão com BD
):
    """
    [MUDANÇA CHAVE] Agora devolve JSON em vez de Redirect.
    Isso permite o login via AJAX sem recarregar a página.
    """
    user = db.query(User).filter(User.username == username).first() # Busca user no BD
    
    # 1. SE ERRO: User não existe OU senha não bate
    if not user or not verify_password(password, user.hashed_password): # type: ignore
        # Devolve 401 + JSON. O JS vai ler e mostrar o SweetAlert
        return JSONResponse(status_code=401, content={"detail": "Usuário ou senha inválidos"})

    # 2. SE SUCESSO: Cria token e guarda na sessão do navegador
    access_token = create_access_token(data={"sub": user.username})
    # request.session = Cookie criptografado no navegador do user
    request.session["access_token"] = access_token 
    
    # Devolve 200 + JSON com pra onde ir. O JS vai fazer o redirect
    return JSONResponse(status_code=200, content={"success": True, "redirect": "/admin"})

@app.get("/admin", tags=["Admin"])
async def admin_page(user: str = Depends(get_current_user)):
    """
    Rota protegida. Só entra se @Depends(get_current_user) retornar o username.
    Se não tiver logado, ele dá 401 antes de chegar aqui.
    """
    return get_html_file("admin.html")

@app.get("/logout", tags=["Auth"])
async def logout(request: Request):
    """Apaga o token da sessão e manda pra home"""
    request.session.pop("access_token", None) # Apaga o cookie de sessão
    return RedirectResponse(url="/", status_code=303) # 303 = Força o navegador a ir pra /

@app.post("/admin/criar", tags=["Admin"])
async def criar_post(
    titulo: str = Form(...), 
    conteudo: str = Form(...), 
    user: str = Depends(get_current_user) # Rota protegida também
):
    """Cria um post novo na lista falsa posts_db"""
    novo_id = len(posts_db) + 1
    posts_db.append({"id": novo_id, "titulo": titulo, "conteudo": conteudo})
    return RedirectResponse(url="/admin", status_code=303)