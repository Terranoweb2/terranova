import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.core.database import get_db
from app.services.ai.documents import DocumentAnalysisService
from app.models.user import User
from app.models.ai_generations import DocumentAnalysis

router = APIRouter()

class DocumentAnalysisRequest(BaseModel):
    queries: Optional[List[str]] = None

class DocumentAnalysisResponse(BaseModel):
    document_url: str
    analysis_result: dict
    document_type: str
    page_count: int

@router.post("/analyze", response_model=DocumentAnalysisResponse)
async def analyze_document(
    file: UploadFile = File(...),
    request: Optional[DocumentAnalysisRequest] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyse un document PDF et répond optionnellement à des questions spécifiques.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Seuls les fichiers PDF sont acceptés"
        )

    try:
        # Créer le dossier de stockage si nécessaire
        upload_dir = os.path.join("uploads", str(current_user.id))
        os.makedirs(upload_dir, exist_ok=True)
        
        # Sauvegarder le fichier
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Analyser le document
        service = DocumentAnalysisService()
        result = await service.analyze_pdf(
            file_path=file_path,
            queries=request.queries if request else None
        )

        # Sauvegarder l'analyse dans la base de données
        db_analysis = DocumentAnalysis(
            user_id=current_user.id,
            document_url=file_path,
            analysis_result=result["analysis"],
            document_type=result["document_type"],
            page_count=result["page_count"]
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)

        return {
            "document_url": file_path,
            "analysis_result": result["analysis"],
            "document_type": result["document_type"],
            "page_count": result["page_count"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[DocumentAnalysisResponse])
async def get_document_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère l'historique des analyses de documents de l'utilisateur.
    """
    analyses = db.query(DocumentAnalysis).filter(
        DocumentAnalysis.user_id == current_user.id
    ).all()
    
    return [
        {
            "document_url": analysis.document_url,
            "analysis_result": analysis.analysis_result,
            "document_type": analysis.document_type,
            "page_count": analysis.page_count
        }
        for analysis in analyses
    ]
