import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Pega a pasta raiz do backend = A:\site_web\backend
BASE_DIR = Path(__file__).resolve().parents[1] 

# 2. Cria o caminho: backend/data/app.db
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True) # Cria a pasta 'data' se não existir
DB_PATH = DATA_DIR / "app.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}" 

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()