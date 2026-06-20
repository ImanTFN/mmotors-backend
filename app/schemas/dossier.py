from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.dossier import TypeDossier, StatutDossier

class DossierCreate(BaseModel):
    vehicle_id: int
    type_dossier: TypeDossier

class DossierUpdate(BaseModel):
    statut: StatutDossier
    commentaire: Optional[str] = None

class DossierResponse(BaseModel):
    id: int
    user_id: int
    vehicle_id: int
    type_dossier: TypeDossier
    statut: StatutDossier
    commentaire: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: int
    dossier_id: int
    nom_fichier: str
    url: str
    created_at: datetime

    class Config:
        from_attributes = True       