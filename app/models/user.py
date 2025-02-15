from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.models.base import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True)
    api_key = Column(String, unique=True, index=True)
    
    # Relations
    text_generations = relationship("TextGeneration", back_populates="user")
    image_generations = relationship("ImageGeneration", back_populates="user")
    music_generations = relationship("MusicGeneration", back_populates="user")
    document_analyses = relationship("DocumentAnalysis", back_populates="user")
