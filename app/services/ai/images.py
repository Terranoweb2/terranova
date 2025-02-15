from typing import Optional
import openai
from app.core.config import settings

class ImageGenerationService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        style: Optional[str] = None,
        num_images: int = 1
    ):
        """
        Génère des images en utilisant DALL-E via l'API OpenAI.
        """
        try:
            # Ajouter le style au prompt si spécifié
            full_prompt = f"{prompt} {style if style else ''}"
            
            response = await openai.Image.acreate(
                prompt=full_prompt,
                n=num_images,
                size=size
            )

            return {
                "images": [img["url"] for img in response["data"]],
                "prompt": full_prompt,
                "size": size,
                "style": style
            }
        except Exception as e:
            raise Exception(f"Erreur lors de la génération d'image: {str(e)}")
