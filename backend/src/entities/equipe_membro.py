"""EquipeMembro entity model."""
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseEntity


class EquipeMembro(BaseEntity):
    """Team member entity."""
    __tablename__ = "equipe_membros"

    equipe_id = Column(Integer, ForeignKey("equipes.id"), nullable=False, index=True)
    estudante_id = Column(Integer, ForeignKey("estudantes.id"), nullable=False, index=True)
    papel = Column(String(50), default="membro")

    # Relationships
    equipe = relationship("Equipe", back_populates="membros")
    estudante = relationship("Estudante", back_populates="equipe_membros")

