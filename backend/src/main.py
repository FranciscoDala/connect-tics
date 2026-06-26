from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

# ===== INICIALIZAÇÃO DA API =====
app = FastAPI(
    title="Connect-Tics API",
    description="API do site Connect-Tics. Serve o frontend e endpoints.",
    version="0.1.0"
)

# ===== MIDDLEWARE CORS =====
# Libera requisições do teu frontend no Vercel pra API
# Sem isso o navegador bloqueia por segurança: CORS error
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://azulula-mbugue.vercel.app",  # Domínio do teu site Vercel
        "http://localhost:5500",              # Pra testar local com Live Server
        "http://localhost:3000"               # Pra testar local com React/Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Libera GET, POST, PUT, DELETE, OPTIONS...
    allow_headers=["*"],  # Libera todos os headers
)

# ===== CAMINHOS DE PASTAS PRA RENDER =====
# Arquivo atual: SITE_WEB/backend/src/main.py
# __file__ = /opt/render/project/src/main.py no Render
# Precisamos chegar na raiz: SITE_WEB/ = /opt/render/project/

# Sobe 2 níveis: src > backend > SITE_WEB = raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Caminho final: SITE_WEB/frontend = onde estão todos os .html
STATIC_DIR = os.path.join(BASE_DIR, "frontend")

# ===== ARQUIVOS ESTÁTICOS =====
# Serve CSS, JS, imagens da pasta /static 
# Ex: /static/style.css -> SITE_WEB/frontend/static/style.css
app.mount("/static", StaticFiles(directory=os.path.join(STATIC_DIR, "static")), name="static")

# ===== FUNÇÃO AUXILIAR =====
def get_html_file(filename: str):
    """
    Função: Verifica se o arquivo .html existe antes de devolver.
    Evita 500 Internal Server Error e mostra 404 se faltar o arquivo.
    """
    file_path = os.path.join(STATIC_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse(
            status_code=404, 
            content={"error": f"Arquivo não encontrado: {filename}", "path": file_path}
        )
    return FileResponse(file_path)

# ===== ROTAS QUE DEVOLVEM HTML =====

@app.get("/", tags=["Pages"])
async def home():
    """
    GET /
    Rota: Página inicial
    Função: Devolve o arquivo index.html da pasta frontend/
    """
    return get_html_file("index.html")

@app.get("/produtos", tags=["Pages"])
async def produtos():
    """
    GET /produtos
    Rota: Página de produtos
    Função: Devolve o arquivo produtos.html
    """
    return get_html_file("produtos.html")

@app.get("/encomendas", tags=["Pages"])
async def encomendas():
    """
    GET /encomendas
    Rota: Página de encomendas/carrinho
    Função: Devolve o arquivo encomendas.html
    """
    return get_html_file("encomendas.html")

@app.get("/login", tags=["Pages"])
async def login():
    """
    GET /login
    Rota: Página de login
    Função: Devolve o arquivo login.html
    """
    return get_html_file("login.html")

@app.get("/quem-somos", tags=["Pages"])
async def quem_somos():
    """
    GET /quem-somos
    Rota: Página institucional
    Função: Devolve o arquivo quem-somos.html
    """
    return get_html_file("quem-somos.html")