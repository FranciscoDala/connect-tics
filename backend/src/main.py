from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

# Cria a instância principal da API FastAPI
# title e description aparecem na doc automática /docs
app = FastAPI(
    title="Connect Tics API",
    description="API do site Connect Tics. Serve o frontend e libera CORS pro Vercel.",
    version="1.0.0"
)

# 1. CORS - Libera o teu frontend que tá no Vercel pra acessar a API
# Sem isso o navegador bloqueia as requisições por segurança
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://azulula-mbugue.vercel.app"], # Domínio do teu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Libera GET, POST, PUT, DELETE, etc
    allow_headers=["*"],  # Libera todos os headers
)

# 2. Caminhos dos arquivos
# BASE_DIR = pasta raiz do projeto, sobe 3 níveis a partir deste arquivo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# STATIC_DIR = pasta onde estão todos os HTML, CSS, JS e imagens
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")

# 3. Servir arquivos estáticos 
# Isso faz o FastAPI servir CSS, JS, imagens da pasta /static
# Ex: /static/style.css vai buscar em frontend/static/style.css
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 4. ROTAS - Cada uma devolve um arquivo HTML direto
# O FileResponse manda o arquivo pro navegador renderizar

@app.get("/", tags=["Paginas"])
async def home():
    """
    Rota: /
    Função: Carrega a página inicial do site.
    Retorna: O arquivo index.html
    """
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/produtos", tags=["Paginas"])
async def produtos():
    """
    Rota: /produtos
    Função: Mostra a página de listagem de produtos.
    Retorna: O arquivo produtos.html
    """
    return FileResponse(os.path.join(STATIC_DIR, "produtos.html"))

@app.get("/encomendas", tags=["Paginas"])
async def encomendas():
    """
    Rota: /encomendas 
    Função: Carrega a página de encomendas/pedidos do cliente.
    Retorna: O arquivo encomendas.html
    """
    return FileResponse(os.path.join(STATIC_DIR, "encomendas.html"))

@app.get("/login", tags=["Paginas"])
async def login():
    """
    Rota: /login
    Função: Mostra a página de login/cadastro de usuário.
    Retorna: O arquivo login.html
    """
    return FileResponse(os.path.join(STATIC_DIR, "login.html"))

@app.get("/quem-somos", tags=["Paginas"])
async def quem_somos():
    """
    Rota: /quem-somos
    Função: Carrega a página 'Quem Somos' com info da empresa.
    Retorna: O arquivo quem-somos.html
    """
    return FileResponse(os.path.join(STATIC_DIR, "quem-somos.html"))

# 5. Bloco pra rodar local E no Render
# O Render injeta a variável PORT automaticamente
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000)) # 8000 local, $PORT no Render
    uvicorn.run("main:app", host="0.0.0.0", port=port)
