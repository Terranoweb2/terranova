from typing import Optional
import openai
from app.core.config import settings

class TextGenerationService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = 1000,
        temperature: Optional[float] = 0.7,
        model: str = "gpt-4"
    ):
        """
        Génère du texte en utilisant le modèle spécifié via l'API OpenAI.
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )

            return {
                "generated_text": response.choices[0].message.content,
                "model_used": model,
                "tokens_used": response.usage.total_tokens
            }
        except Exception as e:
            raise Exception(f"Erreur lors de la génération de texte: {str(e)}")
