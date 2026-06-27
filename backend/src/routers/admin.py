from fastapi import APIRouter, Depends, HTTPException, Form, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from database.database import get_db
from database.models import User
from core.security import hash_password, get_current_user
from schemas.user import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_deps(db: Session = Depends(get_db), me: User = Depends(get_current_user)): 
    return db, me

@router.get("/users", response_model=List[UserOut])
def listar_users(deps = Depends(get_deps)):
    return deps[0].query(User).order_by(User.id).all()

@router.post("/users/add", response_model=UserOut, status_code=201)
def criar_user(username: str = Form(...), password: str = Form(...), deps = Depends(get_deps)):
    db, _ = deps
    if not password or len(password) < 6: # <-- BLINDAGEM
        raise HTTPException(422, "Senha precisa ter 6+ caracteres.")
        
    try:
        data = UserCreate(username=username, password=password) # Valida regex
    except Exception as e:
        raise HTTPException(422, str(e))

    try:
        u = User(username=data.username, hashed_password=hash_password(data.password))
        db.add(u); db.commit(); db.refresh(u); return u
    except IntegrityError: 
        db.rollback(); raise HTTPException(409, "Username já existe.")
    except Exception as e: # <-- Loga o erro real no terminal
        db.rollback()
        print(f"ERRO 500 CRIAR USER: {e}") # <-- Olha no terminal do uvicorn
        raise HTTPException(500, "Erro interno ao criar usuário.")

@router.post("/users/edit/{user_id}", response_model=UserOut)
def editar_user(user_id: int, username: str = Form(...), password: str = Form(None), deps = Depends(get_deps)): # <-- Form(None)
    db, _ = deps
    data = UserUpdate(username=username, password=password) # password=None = não altera
    u = db.query(User).filter(User.id == user_id).first()
    if not u: raise HTTPException(404, "Usuário não encontrado.")
    if db.query(User).filter(User.username == data.username, User.id!= user_id).first(): raise HTTPException(409, "Username em uso.")
    u.username = data.username
    if data.password: u.hashed_password = hash_password(data.password) # <-- Só hasha se veio
    db.commit(); db.refresh(u); return u



@router.post("/users/delete/{user_id}", status_code=204)
def apagar_user(user_id: int, deps = Depends(get_deps)):
    db, me = deps
    if user_id == 1: raise HTTPException(403, "Não pode apagar o admin principal.")
    if user_id == me.id: raise HTTPException(403, "Não pode apagar a si mesmo.")
    u = db.query(User).filter(User.id == user_id).first()
    if not u: raise HTTPException(404, "Usuário não encontrado.")
    db.delete(u); db.commit()