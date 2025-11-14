"""Equipe entity model."""
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseEntity


class Equipe(BaseEntity):
    """Team entity."""
    __tablename__ = "equipes"

    nome = Column(String(255), nullable=False)
    escola_id = Column(Integer, ForeignKey("escolas.id"), nullable=False, index=True)
    ano_edicao = Column(Integer, nullable=False)
    categoria = Column(String(100))
    lider_id = Column(Integer, ForeignKey("estudantes.id"), index=True)
    status = Column(String(50), default="formando")

    # Relationships
    escola = relationship("Escola", back_populates="equipes")
    lider = relationship("Estudante", foreign_keys=[lider_id], back_populates="equipes_lideradas")
    membros = relationship("EquipeMembro", back_populates="equipe", cascade="all, delete-orphan")

