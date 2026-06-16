from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.dossier import Dossier
from app.models.user import User
from app.schemas.dossier import DossierCreate, DossierUpdate, DossierResponse
from app.utils.auth import get_current_user, get_current_admin

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