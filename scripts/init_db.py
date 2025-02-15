import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from app.core.config import settings
from app.models.base import Base
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.core.database import SessionLocal

def init_db():
    # Créer la base de données et les tables
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    
    # Créer un utilisateur admin par défaut
    db = SessionLocal()
    admin_user = db.query(User).filter(User.email == "admin@terranova.ai").first()
    
    if not admin_user:
        admin_user = User(
            email="admin@terranova.ai",
            hashed_password=get_password_hash("admin123"),  # À changer en production !
            full_name="Admin Terranova",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print("Utilisateur admin créé avec succès !")
    
    db.close()

if __name__ == "__main__":
    print("Initialisation de la base de données...")
    init_db()
    print("Base de données initialisée avec succès !")
