from sqlalchemy import Column, String, Integer, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship

from app.models.base import Base

class TextGeneration(Base):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    prompt = Column(String, nullable=False)
    generated_text = Column(String)
    model = Column(String, nullable=False)
    tokens_used = Column(Integer)
    temperature = Column(Float)
    
    user = relationship("User", back_populates="text_generations")

class ImageGeneration(Base):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    prompt = Column(String, nullable=False)
    image_url = Column(String)
    model = Column(String, nullable=False)
    size = Column(String)
    style = Column(String)
    
    user = relationship("User", back_populates="image_generations")

class MusicGeneration(Base):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    prompt = Column(String, nullable=False)
    music_url = Column(String)
    model = Column(String, nullable=False)
    duration = Column(Integer)  # en secondes
    genre = Column(String)
    
    user = relationship("User", back_populates="music_generations")

class DocumentAnalysis(Base):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    document_url = Column(String, nullable=False)
    analysis_result = Column(JSON)
    document_type = Column(String)
    page_count = Column(Integer)
    
    user = relationship("User", back_populates="document_analyses")
