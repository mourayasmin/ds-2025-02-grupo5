"""EquipeMembro DTOs."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class EquipeMembroBase(BaseModel):
    """Base equipe membro schema."""
    equipe_id: int
    estudante_id: int
    papel: str = "membro"


class EquipeMembroCreate(EquipeMembroBase):
    """Schema for creating equipe membro."""
    pass


class EquipeMembroUpdate(BaseModel):
    """Schema for updating equipe membro."""
    papel: Optional[str] = None


class EquipeMembroResponse(EquipeMembroBase):
    """Schema for equipe membro response."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

