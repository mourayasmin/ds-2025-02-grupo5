"""Escola DTOs."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class EscolaBase(BaseModel):
    """Base escola schema."""
    nome: str
    cidade: str
    estado: str = "GO"
    endereco: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    diretor_nome: Optional[str] = None
    ativo: bool = True
    valida: bool = False


class EscolaCreate(EscolaBase):
    """Schema for creating escola."""
    pass


class EscolaUpdate(BaseModel):
    """Schema for updating escola."""
    nome: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    endereco: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    diretor_nome: Optional[str] = None
    ativo: Optional[bool] = None
    status: Optional[bool] = None


class EscolaResponse(EscolaBase):
    """Schema for escola response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

