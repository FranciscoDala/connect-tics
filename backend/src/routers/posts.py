import enum
import shutil
import uuid
import logging
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from database.database import get_db
from database.models import Post as PostModel, PostImage as PostImageModel, Category as CategoryModel
from schemas.posts import PostOut, PostType

router = APIRouter(prefix="/posts", tags=["posts"])
logger = logging.getLogger(__name__)
# ===================================================================
# CORRIGIDO V33: 3x.parent PRA CHEGAR NA RAIZ DO PROJETO
# ===================================================================
ROUTERS_DIR = Path(__file__).resolve().parent # /src/backend/src/routers
SRC_DIR = ROUTERS_DIR.parent # /src/backend/src
BACKEND_DIR = SRC_DIR.parent # /src/backend
PROJECT_ROOT = BACKEND_DIR.parent # /src <-- RAIZ AQUI

STATIC_DIR = PROJECT_ROOT / "frontend" / "static" # /src/frontend/static
UPLOAD_DIR = STATIC_DIR / "assets" / "img" / "uploads" # /src/frontend/static/assets/img/uploads
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
BASE_URL_PATH = "/static/assets/img/uploads" # URL que o browser usa

logger.info(f"====================================")
logger.info(f"PROJECT_ROOT: {PROJECT_ROOT.resolve()}") # Tem que dar /src
logger.info(f"UPLOAD_DIR FIXO: {UPLOAD_DIR.resolve()}") # Tem que dar /src/frontend/static/...
logger.info(f"EXISTE? {UPLOAD_DIR.exists()}")
logger.info(f"====================================")
# ===================================================================


def _save_upload(file: UploadFile | None) -> str | None:
    if not file or not file.filename: return None
    ext = Path(file.filename).suffix.lower()
    filename = f"{uuid.uuid4().hex}{ext}"
    path = UPLOAD_DIR / filename
    with path.open("wb") as buffer: shutil.copyfileobj(file.file, buffer)
    return f"{BASE_URL_PATH}/{filename}"

def _build_post_out(post: PostModel, category_name: str) -> dict:
    return {
        "id": post.id,
        "category_id": post.category_id,
        "category_name": category_name or "Sem Categoria",
        "title": post.title,
        "type": post.type.value if isinstance(post.type, enum.Enum) else post.type,
        "is_highlighted": post.is_highlighted,
        "content": post.content,
        "price": post.price,
        "link": post.link,
        "cover_image": post.cover_image,
        "created_at": post.created_at,
        "images": [{"id": i.id, "image_url": i.image_url, "likes": i.likes, "dislikes": i.dislikes} for i in post.images]
    }

def _sync_images(db: Session, post: PostModel, files: list[UploadFile]):
    for img in post.images:
        file_path = UPLOAD_DIR / Path(img.image_url).name
        if file_path.exists():
            try: file_path.unlink()
            except: pass
    db.query(PostImageModel).filter(PostImageModel.post_id == post.id).delete(synchronize_session=False)

    for f in files:
        if f and f.filename:
            url = _save_upload(f)
            if url: db.add(PostImageModel(post_id=post.id, image_url=url))
    db.commit()
    db.refresh(post)

@router.get("", response_model=list[PostOut])
def read_posts(limit: int = 100, skip: int = 0, db: Session = Depends(get_db)):
    stmt = (
        select(PostModel)
     .options(joinedload(PostModel.images), joinedload(PostModel.category))
     .order_by(PostModel.created_at.desc())
     .offset(skip)
     .limit(limit)
    )
    posts = db.execute(stmt).unique().scalars().all()
    return [_build_post_out(p, p.category.name if p.category else "") for p in posts]
@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(
    category_id: int | None = Form(None), # <-- CORRIGIDO V34: Aceita vazio pra não dar 422
    title: str = Form(...),
    type: PostType = Form(...),
    is_highlighted: bool = Form(False),
    content: str | None = Form(None),
    price: float | None = Form(None),
    link: str | None = Form(None),
    cover_image: UploadFile | None = File(None),
    images: list[UploadFile] = File([]), # <-- CORRIGIDO V34: [] em vez de None. Aceita multi vazio
    db: Session = Depends(get_db)
):
    if not category_id: raise HTTPException(status_code=400, detail="category_id obrigatório") # <-- Validação manual
    category = db.get(CategoryModel, category_id)
    if not category: raise HTTPException(status_code=404, detail=f"Category {category_id} not found")

    cover_url = _save_upload(cover_image)

    db_post = PostModel(
        category_id=category_id,
        title=title,
        type=type,
        is_highlighted=is_highlighted,
        content=content,
        price=price,
        link=link,
        cover_image=cover_url
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    if type == PostType.fotos:
        if not images or not any(f.filename for f in images):
            raise HTTPException(status_code=400, detail="Type 'fotos' precisa de ao menos 1 imagem")
        _sync_images(db, db_post, images)

    db.refresh(db_post, attribute_names=['images'])
    return _build_post_out(db_post, category.name)

@router.get("/{post_id}", response_model=PostOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    stmt = select(PostModel).options(joinedload(PostModel.images), joinedload(PostModel.category)).filter(PostModel.id == post_id)
    post = db.execute(stmt).scalar_one_or_none()
    if not post: raise HTTPException(status_code=404, detail="Post not found")
    return _build_post_out(post, post.category.name if post.category else "")

@router.put("/{post_id}", response_model=PostOut)
async def update_post(
    post_id: int,
    category_id: int = Form(...),
    title: str = Form(...),
    type: PostType = Form(...),
    is_highlighted: bool = Form(False),
    content: str | None = Form(None),
    price: float | None = Form(None),
    link: str | None = Form(None),
    cover_image: UploadFile | None = File(None),
    images: list[UploadFile] = File([]), # <-- CORRIGIDO V34: [] em vez de None
    existing_images: list[str] = Form([]),
    db: Session = Depends(get_db)
):
    db_post = db.get(PostModel, post_id)
    if not db_post: raise HTTPException(status_code=404, detail="Post not found")
    category = db.get(CategoryModel, category_id)
    if not category: raise HTTPException(status_code=404, detail=f"Category {category_id} not found")

    if cover_image and cover_image.filename:
        if db_post.cover_image:
            old_file = UPLOAD_DIR / Path(db_post.cover_image).name
            if old_file.exists(): old_file.unlink(missing_ok=True)
        db_post.cover_image = _save_upload(cover_image)

    db_post.category_id = category_id
    db_post.title = title
    db_post.type = type
    db_post.is_highlighted = is_highlighted
    db_post.content = content
    db_post.price = price
    db_post.link = link

    if type == PostType.fotos:
        urls_to_keep = set(existing_images)
        for img in list(db_post.images):
            if img.image_url not in urls_to_keep:
                file_path = UPLOAD_DIR / Path(img.image_url).name
                if file_path.exists(): file_path.unlink(missing_ok=True)
                db.delete(img)
        if images:
            for f in images:
                if f and f.filename:
                    url = _save_upload(f)
                    if url: db.add(PostImageModel(post_id=db_post.id, image_url=url))

    db.commit()
    db.refresh(db_post, attribute_names=['images'])
    return _build_post_out(db_post, category.name)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.get(PostModel, post_id)
    if not db_post: raise HTTPException(status_code=404, detail="Post not found")
    files_to_delete = [UPLOAD_DIR / Path(db_post.cover_image).name] if db_post.cover_image else []
    files_to_delete.extend([UPLOAD_DIR / Path(img.image_url).name for img in db_post.images])
    db.delete(db_post)
    db.commit()
    for f in files_to_delete: f.unlink(missing_ok=True)
    return

@router.post("/images/{image_id}/like")
def like_image(image_id: int, db: Session = Depends(get_db)):
    img = db.get(PostImageModel, image_id)
    if not img: raise HTTPException(404)
    img.likes += 1
    db.commit()
    return {"ok": True, "likes": img.likes}

@router.post("/images/{image_id}/dislike")
def dislike_image(image_id: int, db: Session = Depends(get_db)):
    img = db.get(PostImageModel, image_id)
    if not img: raise HTTPException(404)
    img.dislikes += 1
    db.commit()
    return {"ok": True, "dislikes": img.dislikes}