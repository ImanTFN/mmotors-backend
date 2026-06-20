from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.database import get_db
from app.models.dossier import Dossier, Document
from app.models.user import User
from app.schemas.dossier import DossierCreate, DossierUpdate, DossierResponse, DocumentResponse
from app.utils.auth import get_current_user, get_current_admin, supabase_client

router = APIRouter(prefix="/dossiers", tags=["Dossiers"])

@router.post("/", response_model=DossierResponse, status_code=201)
def create_dossier(
    dossier_data: DossierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_dossier = Dossier(
        user_id=current_user.id,
        vehicle_id=dossier_data.vehicle_id,
        type_dossier=dossier_data.type_dossier
    )
    db.add(new_dossier)
    db.commit()
    db.refresh(new_dossier)
    return new_dossier

@router.get("/mes-dossiers", response_model=List[DossierResponse])
def get_mes_dossiers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Dossier).filter(Dossier.user_id == current_user.id).all()

@router.get("/", response_model=List[DossierResponse])
def get_all_dossiers(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    return db.query(Dossier).all()

@router.patch("/{dossier_id}", response_model=DossierResponse)
def update_dossier(
    dossier_id: int,
    dossier_data: DossierUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    dossier = db.query(Dossier).filter(Dossier.id == dossier_id).first()
    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier introuvable")
    for key, value in dossier_data.model_dump(exclude_unset=True).items():
        setattr(dossier, key, value)
    db.commit()
    db.refresh(dossier)
    return dossier

@router.post("/{dossier_id}/documents", response_model=DocumentResponse, status_code=201)
def upload_document(
    dossier_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dossier = db.query(Dossier).filter(Dossier.id == dossier_id).first()
    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier introuvable")
    if dossier.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ce dossier ne vous appartient pas")

    file_content = file.file.read()
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    storage_path = f"dossier_{dossier_id}/{unique_filename}"

    supabase_client.storage.from_("dossiers-documents").upload(
        storage_path, file_content, {"content-type": file.content_type}
    )

    public_url = supabase_client.storage.from_("dossiers-documents").get_public_url(storage_path)

    new_document = Document(
        dossier_id=dossier_id,
        nom_fichier=file.filename,
        url=public_url
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document

@router.get("/{dossier_id}/documents", response_model=List[DocumentResponse])
def get_documents(
    dossier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dossier = db.query(Dossier).filter(Dossier.id == dossier_id).first()
    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier introuvable")
    if dossier.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès refusé")
    return db.query(Document).filter(Document.dossier_id == dossier_id).all()