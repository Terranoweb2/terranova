from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.core.database import get_db
from app.services.ai.images import ImageGenerationService
from app.models.user import User
from app.models.ai_generations import ImageGeneration

router = APIRouter()

class ImageGenerationRequest(BaseModel):
    prompt: str
    size: Optional[str] = "1024x1024"
    style: Optional[str] = None
    num_images: Optional[int] = 1

class ImageGenerationResponse(BaseModel):
    images: List[str]
    prompt: str
    size: str
    style: Optional[str]

@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(
    request: ImageGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Génère des images à partir d'un prompt en utilisant DALL-E.
    """
    try:
        service = ImageGenerationService()
        result = await service.generate(
            prompt=request.prompt,
            size=request.size,
            style=request.style,
            num_images=request.num_images
        )

        # Sauvegarder chaque génération dans la base de données
        for image_url in result["images"]:
            db_generation = ImageGeneration(
                user_id=current_user.id,
                prompt=request.prompt,
                image_url=image_url,
                model="dall-e",
                size=request.size,
                style=request.style
            )
            db.add(db_generation)
        
        db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[ImageGenerationResponse])
async def get_image_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère l'historique des générations d'images de l'utilisateur.
    """
    generations = db.query(ImageGeneration).filter(
        ImageGeneration.user_id == current_user.id
    ).all()
    
    return [
        {
            "images": [gen.image_url],
            "prompt": gen.prompt,
            "size": gen.size,
            "style": gen.style
        }
        for gen in generations
    ]
