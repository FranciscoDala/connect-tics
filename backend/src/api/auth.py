from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User
from core.security import verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api", tags=["Auth"]) # <-- prefix fica só aqui

@router.post("/login")
async def login_post(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "redirect": "/admin"}

@router.post("/logout")
async def logout():
    return JSONResponse(status_code=200, content={"success": True})

@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username}