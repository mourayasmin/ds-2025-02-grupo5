"""EquipeMembro repository."""
from typing import Optional, List
from sqlalchemy.orm import Session
from src.entities.equipe_membro import EquipeMembro
from .base_repository import BaseRepository


class EquipeMembroRepository(BaseRepository[EquipeMembro]):
    """Repository for EquipeMembro entity."""

    def __init__(self, db: Session):
        super().__init__(EquipeMembro, db)

    def get_by_equipe_id(self, equipe_id: int) -> List[EquipeMembro]:
        """Get membros by equipe ID."""
        return self.db.query(EquipeMembro).filter(EquipeMembro.equipe_id == equipe_id).all()

    def get_by_estudante_id(self, estudante_id: int) -> List[EquipeMembro]:
        """Get membros by estudante ID."""
        return self.db.query(EquipeMembro).filter(EquipeMembro.estudante_id == estudante_id).all()

    def get_by_equipe_and_estudante(self, equipe_id: int, estudante_id: int) -> Optional[EquipeMembro]:
        """Get membro by equipe ID and estudante ID."""
        return self.db.query(EquipeMembro).filter(
            EquipeMembro.equipe_id == equipe_id,
            EquipeMembro.estudante_id == estudante_id
        ).first()

