from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum

class PostType(str, Enum):
    normal = "normal"
    fotos = "fotos"

class PostImageOut(BaseModel):
    id: int
    image_url: str
    likes: int = 0 # <-- ADICIONA ISSO
    dislikes: int = 0 # <-- ADICIONA ISSO
    model_config = ConfigDict(from_attributes = True) # Pydantic v2

class PostOut(BaseModel): # Resposta da API
    id: int
    title: str
    type: PostType
    category_id: int
    category_name: str
    content: str | None = None
    price: float | None = None
    link: str | None = None
    cover_image: str | None = None
    is_highlighted: bool
    images: list[PostImageOut] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes = True)

class PostCreate(BaseModel): # Body do POST
    title: str
    category_id: int
    type: PostType
    content: str | None = None
    price: float | None = None
    link: str | None = None
    cover_image: str | None = None
    is_highlighted: bool = False
    images: list[str] = Field(default_factory=list)

class PostUpdate(BaseModel): # Body do PUT/PATCH. Tudo opcional
    title: str | None = None
    category_id: int | None = None
    type: PostType | None = None
    content: str | None = None
    price: float | None = None
    link: str | None = None
    cover_image: str | None = None
    is_highlighted: bool | None = None
    images: list[str] | None = None