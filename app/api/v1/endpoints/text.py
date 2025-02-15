from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.core.security import get_current_user
from app.services.ai.text import TextGenerationService

router = APIRouter()

class TextGenerationRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    model: Optional[str] = "gpt-4"

class TextGenerationResponse(BaseModel):
    generated_text: str
    model_used: str
    tokens_used: int

@router.post("/generate", response_model=TextGenerationResponse)
async def generate_text(
    request: TextGenerationRequest,
    current_user = Depends(get_current_user)
):
    """
    Génère du texte à partir d'un prompt en utilisant le modèle spécifié.
    """
    try:
        service = TextGenerationService()
        result = await service.generate(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            model=request.model
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
