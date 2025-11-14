"""Inscricao DTOs."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InscricaoBase(BaseModel):
    """Base inscricao schema."""
    estudante_id: int
    escola_id: int
    ano_edicao: int
    categoria: Optional[str] = None
    equipe_nome: Optional[str] = None
    observacoes: Optional[str] = None


class InscricaoCreate(InscricaoBase):
    """Schema for creating inscricao."""
    pass


class InscricaoUpdate(BaseModel):
    """Schema for updating inscricao."""
    estudante_id: Optional[int] = None
    escola_id: Optional[int] = None
    ano_edicao: Optional[int] = None
    status: Optional[str] = None
    categoria: Optional[str] = None
    equipe_nome: Optional[str] = None
    observacoes: Optional[str] = None


class InscricaoResponse(InscricaoBase):
    """Schema for inscricao response."""
    id: int
    status: str
    data_inscricao: datetime
    data_confirmacao: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

