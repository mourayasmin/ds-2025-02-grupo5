"""Inscricao entity model."""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseEntity


class Inscricao(BaseEntity):
    """Subscription/Registration entity."""
    __tablename__ = "inscricoes"

    estudante_id = Column(Integer, ForeignKey("estudantes.id"), nullable=False, index=True)
    escola_id = Column(Integer, ForeignKey("escolas.id"), nullable=False, index=True)
    ano_edicao = Column(Integer, nullable=False, index=True)
    status = Column(String(50), default="pendente", index=True)
    categoria = Column(String(100))
    equipe_nome = Column(String(255))
    observacoes = Column(Text)
    data_inscricao = Column(DateTime, default=datetime.utcnow)
    data_confirmacao = Column(DateTime)

    # Relationships
    estudante = relationship("Estudante", back_populates="inscricoes")
    escola = relationship("Escola", back_populates="inscricoes")

