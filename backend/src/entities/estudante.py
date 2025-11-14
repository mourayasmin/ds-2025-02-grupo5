"""Estudante entity model."""
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseEntity


class Estudante(BaseEntity):
    """Student entity."""
    __tablename__ = "estudantes"

    nome_completo = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    data_nascimento = Column(Date, nullable=False)
    email = Column(String(255), nullable=False)
    telefone = Column(String(20))
    escola_id = Column(Integer, ForeignKey("escolas.id"), nullable=False, index=True)
    serie_ano = Column(String(20), nullable=False)
    turno = Column(String(20))

    # Relationships
    escola = relationship("Escola", back_populates="estudantes")
    inscricoes = relationship("Inscricao", back_populates="estudante", cascade="all, delete-orphan")
    equipes_lideradas = relationship("Equipe", foreign_keys="[Equipe.lider_id]", back_populates="lider")
    equipe_membros = relationship("EquipeMembro", back_populates="estudante", cascade="all, delete-orphan")

