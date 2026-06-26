from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

# ===== INICIALIZAÇÃO DA API =====
app = FastAPI(title="Connect-Tics API")

# ===== MIDDLEWARE CORS =====
# Libera requisições do teu frontend no Vercel
# Sem isso o navegador bloqueia por segurança
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://azulula-mbugue.vercel.app"], # Domínio do teu site Vercel
    allow_credentials=True,
    allow_methods=["*"],  # Libera GET, POST, PUT, DELETE...
    allow_headers=["*"],
)

# ===== CAMINHOS DE PASTAS CORRIGIDOS PRA RENDER =====
# Arquivo atual: SITE_WEB/backend/src/main.py
# Precisamos subir 4 níveis: src > backend > SITE_WEB > raiz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Caminho: SITE_WEB/frontend/static
STATIC_DIR = os.path.join(os.path.dirname(__file__), "frontend", "static")

# ===== ARQUIVOS ESTÁTICOS =====
# Serve tudo da pasta /static -> CSS, JS, imagens
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ===== ROTAS QUE DEVOLVEM HTML =====

@app.get("/")
async def home():
    """
    GET /
    Função: Devolve o arquivo index.html da pasta static
    """
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/produtos")
async def produtos():
    """
    GET /produtos
    Função: Devolve a página produtos.html
    """
    return FileResponse(os.path.join(STATIC_DIR, "produtos.html"))

@app.get("/encomendas")
async def encomendas():
    """
    GET /encomendas
    Função: Devolve a página encomendas.html
    """
    return FileResponse(os.path.join(STATIC_DIR, "encomendas.html"))

@app.get("/login")
async def login():
    """
    GET /login
    Função: Devolve a página login.html
    """
    return FileResponse(os.path.join(STATIC_DIR, "login.html"))

@app.get("/quem-somos")
async def quem_somos():
    """
    GET /quem-somos
    Função: Devolve a página quem-somos.html
    """
    return FileResponse(os.path.join(STATIC_DIR, "quem-somos.html"))