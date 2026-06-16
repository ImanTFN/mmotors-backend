from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    marque = Column(String, nullable=False)
    modele = Column(String, nullable=False)
    annee = Column(Integer, nullable=False)
    kilometrage = Column(Integer, nullable=False)
    prix = Column(Float, nullable=False)
    motorisation = Column(String, nullable=False)
    disponible_achat = Column(Boolean, default=True)
    disponible_location = Column(Boolean, default=False)
    prix_location_mois = Column(Float, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())