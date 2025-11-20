"""Escola entity model."""
from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship
from .base import BaseEntity


class Escola(BaseEntity):
    """School entity."""
    __tablename__ = "escolas"

    nome = Column(String(255), nullable=False)
    endereco = Column(Text)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False, default="GO")
    cep = Column(String(10))
    telefone = Column(String(20))
    email = Column(String(255))
    diretor_nome = Column(String(255))
    ativo = Column(Boolean, default=True)
    valida = Column(Boolean, default=False)

    # Relationships
    estudantes = relationship("Estudante", back_populates="escola", cascade="all, delete-orphan")
    inscricoes = relationship("Inscricao", back_populates="escola")
    equipes = relationship("Equipe", back_populates="escola", cascade="all, delete-orphan")

