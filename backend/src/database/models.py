import enum 
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base # . = mesma pasta

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class PostType(str, enum.Enum):
    normal = "normal"
    fotos = "fotos"

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    posts = relationship("Post", back_populates="category")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    title = Column(String(255), nullable=False, index=True)
    type = Column(SQLEnum(PostType), nullable=False, default=PostType.normal)
    content = Column(Text, nullable=True) # Só pra 'normal'
    price = Column(Float, nullable=True) # Só pra 'normal'
    link = Column(String(500), nullable=True) # Só pra 'normal'
    cover_image = Column(String(500), nullable=True) # Só pra 'normal'
    is_highlighted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="posts")
    images = relationship("PostImage", back_populates="post", cascade="all, delete-orphan") # Apaga fotos se apagar o post

class PostImage(Base): # <-- SÓ 1 VEZ AGORA
    __tablename__ = "post_images"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False) # <-- ondelete DENTRO do ForeignKey
    image_url = Column(String(500), nullable=False)
    likes = Column(Integer, default=0, nullable=False) # <-- Like por foto
    dislikes = Column(Integer, default=0, nullable=False) # <-- Dislike por foto

    post = relationship("Post", back_populates="images")