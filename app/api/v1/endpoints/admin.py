from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.security import get_current_user
from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.ai_generations import (
    TextGeneration,
    ImageGeneration,
    MusicGeneration,
    DocumentAnalysis
)

router = APIRouter()

class UserStats(BaseModel):
    total_text_generations: int
    total_image_generations: int
    total_music_generations: int
    total_document_analyses: int

class UserAdminResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    role: UserRole
    is_active: bool
    stats: UserStats

    class Config:
        from_attributes = True

def check_admin(user: User):
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )

@router.get("/users", response_model=List[UserAdminResponse])
async def get_all_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les utilisateurs avec leurs statistiques.
    Réservé aux administrateurs.
    """
    check_admin(current_user)
    
    users = db.query(User).all()
    result = []
    
    for user in users:
        stats = UserStats(
            total_text_generations=db.query(TextGeneration)
                .filter(TextGeneration.user_id == user.id)
                .count(),
            total_image_generations=db.query(ImageGeneration)
                .filter(ImageGeneration.user_id == user.id)
                .count(),
            total_music_generations=db.query(MusicGeneration)
                .filter(MusicGeneration.user_id == user.id)
                .count(),
            total_document_analyses=db.query(DocumentAnalysis)
                .filter(DocumentAnalysis.user_id == user.id)
                .count()
        )
        
        result.append(UserAdminResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            stats=stats
        ))
    
    return result

@router.put("/users/{user_id}/activate", response_model=UserAdminResponse)
async def toggle_user_activation(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Active ou désactive un utilisateur.
    Réservé aux administrateurs.
    """
    check_admin(current_user)
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
    
    # Récupérer les statistiques
    stats = UserStats(
        total_text_generations=db.query(TextGeneration)
            .filter(TextGeneration.user_id == user.id)
            .count(),
        total_image_generations=db.query(ImageGeneration)
            .filter(ImageGeneration.user_id == user.id)
            .count(),
        total_music_generations=db.query(MusicGeneration)
            .filter(MusicGeneration.user_id == user.id)
            .count(),
        total_document_analyses=db.query(DocumentAnalysis)
            .filter(DocumentAnalysis.user_id == user.id)
            .count()
    )
    
    return UserAdminResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        stats=stats
    )

class SystemStats(BaseModel):
    total_users: int
    active_users: int
    total_generations: int
    generations_by_type: dict

@router.get("/stats", response_model=SystemStats)
async def get_system_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les statistiques globales du système.
    Réservé aux administrateurs.
    """
    check_admin(current_user)
    
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    
    generations_by_type = {
        "text": db.query(func.count(TextGeneration.id)).scalar(),
        "image": db.query(func.count(ImageGeneration.id)).scalar(),
        "music": db.query(func.count(MusicGeneration.id)).scalar(),
        "document": db.query(func.count(DocumentAnalysis.id)).scalar()
    }
    
    total_generations = sum(generations_by_type.values())
    
    return SystemStats(
        total_users=total_users,
        active_users=active_users,
        total_generations=total_generations,
        generations_by_type=generations_by_type
    )
