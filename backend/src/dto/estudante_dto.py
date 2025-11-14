"""Estudante DTOs."""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class EstudanteBase(BaseModel):
    """Base estudante schema."""
    nome_completo: str
    cpf: str
    data_nascimento: date
    email: EmailStr
    escola_id: int
    serie_ano: str
    telefone: Optional[str] = None
    turno: Optional[str] = None


class EstudanteCreate(EstudanteBase):
    """Schema for creating estudante."""
    pass


class EstudanteUpdate(BaseModel):
    """Schema for updating estudante."""
    nome_completo: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[date] = None
    email: Optional[EmailStr] = None
    escola_id: Optional[int] = None
    serie_ano: Optional[str] = None
    telefone: Optional[str] = None
    turno: Optional[str] = None


class EstudanteResponse(EstudanteBase):
    """Schema for estudante response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

