from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VehicleCreate(BaseModel):
    marque: str
    modele: str
    annee: int
    kilometrage: int
    prix: float
    motorisation: str
    disponible_achat: bool = True
    disponible_location: bool = False
    prix_location_mois: Optional[float] = None
    image_url: Optional[str] = None

class VehicleUpdate(BaseModel):
    marque: Optional[str] = None
    modele: Optional[str] = None
    annee: Optional[int] = None
    kilometrage: Optional[int] = None
    prix: Optional[float] = None
    motorisation: Optional[str] = None
    disponible_achat: Optional[bool] = None
    disponible_location: Optional[bool] = None
    prix_location_mois: Optional[float] = None
    image_url: Optional[str] = None

class VehicleResponse(BaseModel):
    id: int
    marque: str
    modele: str
    annee: int
    kilometrage: int
    prix: float
    motorisation: str
    disponible_achat: bool
    disponible_location: bool
    prix_location_mois: Optional[float]
    image_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True