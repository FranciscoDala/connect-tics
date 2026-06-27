from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from database.database import get_db
from database.models import Category

router = APIRouter(prefix="/categories", tags=["categories"])

class CategoryOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str

# 1. LISTAR TODAS - GET /admin/categories
@router.get("", response_model=list[CategoryOut]) # <-- SEM / no fim. Isso evita 404
def read_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.name.asc()).all()

# 2. CRIAR - POST /admin/categories
@router.post("", response_model=CategoryOut, status_code=201) # <-- SEM / no fim
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Nome não pode ser vazio")
    if db.query(Category).filter(Category.name.ilike(name)).first():
        raise HTTPException(status_code=400, detail="Categoria já existe")
    db_cat = Category(name=name)
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

# 3. EDITAR - PUT /admin/categories/{id}
@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    db_cat = db.query(Category).filter(Category.id == category_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Nome não pode ser vazio")
    
    # Evita duplicar nome em outro id
    if db.query(Category).filter(Category.name.ilike(name), Category.id!= category_id).first():
        raise HTTPException(status_code=400, detail="Já existe outra categoria com esse nome")
    
    db_cat.name = name
    db.commit()
    db.refresh(db_cat)
    return db_cat

# 4. APAGAR - DELETE /admin/categories/{id}
@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_cat = db.query(Category).filter(Category.id == category_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    # Segurança: não deixa apagar se tiver post
    if db.query(Post).filter(Post.category_id == category_id).first(): # <-- Precisa importar Post
        raise HTTPException(status_code=400, detail="Não pode apagar. Categoria tem posts vinculados.")
        
    db.delete(db_cat)
    db.commit()
    return None