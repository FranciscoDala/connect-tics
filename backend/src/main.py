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

# ===== CAMINHOS DE PASTAS PRA RENDER - AJUSTADO PRA STATIC =====
# Sobe 3 níveis: main.py -> src -> backend -> RAIZ
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Caminho final: RAIZ/frontend/static = onde estão todos os .html agora
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")

# ===== ARQUIVOS ESTÁTICOS =====
# Serve CSS, JS, imagens da mesma pasta /static 
# Ex: /static/style.css -> RAIZ/frontend/static/style.css
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ===== FUNÇÃO AUXILIAR =====
def get_html_file(filename: str):
    """
    Verifica se o arquivo .html existe antes de devolver.
    Evita 500 e mostra 404 + caminho se faltar o arquivo. 
    """
    file_path = os.path.join(STATIC_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse(
            status_code=404, 
            content={"error": f"Arquivo não encontrado: {filename}", "path": file_path}
        )
    return FileResponse(file_path)

# ===== ROTAS QUE DEVOLVEM HTML - TUAS ROTAS INTACTAS =====

@app.get("/", tags=["Pages"])
async def home():
    return get_html_file("index.html")

@app.get("/produtos", tags=["Pages"])
async def produtos():
    return get_html_file("produtos.html")

@app.get("/encomendas", tags=["Pages"])
async def encomendas():
    return get_html_file("encomendas.html")

@app.get("/login", tags=["Pages"])
async def login():
    return get_html_file("login.html")

@app.get("/quem-somos", tags=["Pages"])
async def quem_somos():
    return get_html_file("quem-somos.html")