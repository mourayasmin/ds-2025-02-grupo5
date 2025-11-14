"""Equipe repository."""
from typing import Optional, List
from sqlalchemy.orm import Session
from src.entities.equipe import Equipe
from .base_repository import BaseRepository


class EquipeRepository(BaseRepository[Equipe]):
    """Repository for Equipe entity."""

    def __init__(self, db: Session):
        super().__init__(Equipe, db)

    def get_by_escola_id(self, escola_id: int) -> List[Equipe]:
        """Get equipes by escola ID."""
        return self.db.query(Equipe).filter(Equipe.escola_id == escola_id).all()

    def get_by_ano_edicao(self, ano_edicao: int) -> List[Equipe]:
        """Get equipes by year."""
        return self.db.query(Equipe).filter(Equipe.ano_edicao == ano_edicao).all()

    def get_by_status(self, status: str) -> List[Equipe]:
        """Get equipes by status."""
        return self.db.query(Equipe).filter(Equipe.status == status).all()

    def get_by_lider_id(self, lider_id: int) -> List[Equipe]:
        """Get equipes by leader ID."""
        return self.db.query(Equipe).filter(Equipe.lider_id == lider_id).all()

