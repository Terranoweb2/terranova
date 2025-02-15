from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.core.database import get_db
from app.services.ai.music import MusicGenerationService
from app.models.user import User
from app.models.ai_generations import MusicGeneration

router = APIRouter()

class MusicGenerationRequest(BaseModel):
    prompt: str
    duration: Optional[int] = 30
    genre: Optional[str] = None

class MusicGenerationResponse(BaseModel):
    music_url: str
    prompt: str
    duration: int
    genre: Optional[str]

@router.post("/generate", response_model=MusicGenerationResponse)
async def generate_music(
    request: MusicGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Génère de la musique basée sur un prompt textuel.
    """
    try:
        service = MusicGenerationService()
        result = await service.generate(
            prompt=request.prompt,
            duration=request.duration,
            genre=request.genre
        )

        # Sauvegarder la génération dans la base de données
        db_generation = MusicGeneration(
            user_id=current_user.id,
            prompt=request.prompt,
            music_url=result["music_url"],
            model="mubert",  # ou le modèle que vous utilisez
            duration=result["duration"],
            genre=result["genre"]
        )
        db.add(db_generation)
        db.commit()
        db.refresh(db_generation)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[MusicGenerationResponse])
async def get_music_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère l'historique des générations de musique de l'utilisateur.
    """
    generations = db.query(MusicGeneration).filter(
        MusicGeneration.user_id == current_user.id
    ).all()
    
    return [
        {
            "music_url": gen.music_url,
            "prompt": gen.prompt,
            "duration": gen.duration,
            "genre": gen.genre
        }
        for gen in generations
    ]
