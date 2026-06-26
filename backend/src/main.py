from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# 1. CORS - Libera teu site Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://azulula-mbugue.vercel.app"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")

# Servir arquivos estáticos (CSS, JS, imagens e HTML)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Rotas que devolvem arquivos HTML direto
@app.get("/")
async def home():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/produtos")
async def produtos():
    return FileResponse(os.path.join(STATIC_DIR, "produtos.html"))

@app.get("/encomendas")
async def encomendas():
    return FileResponse(os.path.join(STATIC_DIR, "encomendas.html"))

@app.get("/login")
async def login():
    return FileResponse(os.path.join(STATIC_DIR, "login.html"))

@app.get("/quem-somos")
async def quem_somos():
    return FileResponse(os.path.join(STATIC_DIR, "quem-somos.html"))
