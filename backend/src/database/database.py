import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. TENTA PEGAR A URL DO SUPABASE PRIMEIRO
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # MODO PRODUÇÃO: SUPABASE POSTGRES
    print(f">>> DATABASE: MODO SUPABASE ATIVO")
    # FIX: Força SSL que o Supabase exige
    if "supabase.co" in DATABASE_URL and "sslmode" not in DATABASE_URL:
        DATABASE_URL += "?sslmode=require"
    
    engine = create_engine(
        DATABASE_URL, 
        pool_pre_ping=True, # Evita conexão morta do Free Tier
        connect_args={"sslmode": "require"} if "supabase.co" in DATABASE_URL else {}
    )
else:
    # MODO DEV: SQLITE LOCAL
    print(f">>> DATABASE: MODO SQLITE LOCAL ATIVO")
    BASE_DIR = Path(__file__).resolve().parents[1] 
    DATA_DIR = BASE_DIR / "data"
    DATA_DIR.mkdir(exist_ok=True)
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