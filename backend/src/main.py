from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# ===== DEBUG TOTAL =====
def find_frontend_dir():
    current_dir = os.path.dirname(__file__)
    for i in range(5):
        test_path = os.path.join(current_dir, "frontend")
        if os.path.exists(test_path):
            return current_dir 
        current_dir = os.path.dirname(current_dir)
    return "NAO_ACHOU" # Se não achar

BASE_DIR = find_frontend_dir()
STATIC_DIR = os.path.join(BASE_DIR, "frontend")

@app.get("/")
def debug():
    return {
        "ARQUIVO_ATUAL": __file__,
        "BASE_DIR_ACHADO": BASE_DIR,
        "STATIC_DIR": STATIC_DIR, 
        "PROCURANDO_INDEX_EM": os.path.join(STATIC_DIR, "index.html"),
        "EXISTE_INDEX?": os.path.exists(os.path.join(STATIC_DIR, "index.html"))
    }