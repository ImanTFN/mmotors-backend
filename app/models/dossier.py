from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TypeDossier(str, enum.Enum):
    achat = "achat"
    location = "location"

class StatutDossier(str, enum.Enum):
    en_attente = "en_attente"
    en_cours = "en_cours"
    valide = "valide"
    refuse = "refuse"

class Dossier(Base):
    __tablename__ = "dossiers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    type_dossier = Column(Enum(TypeDossier), nullable=False)
    statut = Column(Enum(StatutDossier), default=StatutDossier.en_attente)
    commentaire = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", backref="dossiers")
    vehicle = relationship("Vehicle", backref="dossiers")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    dossier_id = Column(Integer, ForeignKey("dossiers.id"), nullable=False)
    nom_fichier = Column(String, nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())    