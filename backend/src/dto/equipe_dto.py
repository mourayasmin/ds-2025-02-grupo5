"""Equipe DTOs."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class EquipeBase(BaseModel):
    """Base equipe schema."""
    nome: str
    escola_id: int
    ano_edicao: int
    categoria: Optional[str] = None
    lider_id: Optional[int] = None
    status: str = "formando"


class EquipeCreate(EquipeBase):
    """Schema for creating equipe."""
    pass


class EquipeUpdate(BaseModel):
    """Schema for updating equipe."""
    nome: Optional[str] = None
    escola_id: Optional[int] = None
    ano_edicao: Optional[int] = None
    categoria: Optional[str] = None
    lider_id: Optional[int] = None
    status: Optional[str] = None


class EquipeResponse(EquipeBase):
    """Schema for equipe response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

