"""Inscricao repository."""
from typing import Optional, List
from sqlalchemy.orm import Session
from src.entities.inscricao import Inscricao
from .base_repository import BaseRepository


class InscricaoRepository(BaseRepository[Inscricao]):
    """Repository for Inscricao entity."""

    def __init__(self, db: Session):
        super().__init__(Inscricao, db)

    def get_by_estudante_id(self, estudante_id: int) -> List[Inscricao]:
        """Get inscricoes by estudante ID."""
        return self.db.query(Inscricao).filter(Inscricao.estudante_id == estudante_id).all()

    def get_by_escola_id(self, escola_id: int) -> List[Inscricao]:
        """Get inscricoes by escola ID."""
        return self.db.query(Inscricao).filter(Inscricao.escola_id == escola_id).all()

    def get_by_ano_edicao(self, ano_edicao: int) -> List[Inscricao]:
        """Get inscricoes by year."""
        return self.db.query(Inscricao).filter(Inscricao.ano_edicao == ano_edicao).all()

    def get_by_status(self, status: str) -> List[Inscricao]:
        """Get inscricoes by status."""
        return self.db.query(Inscricao).filter(Inscricao.status == status).all()

    def get_by_estudante_and_ano(self, estudante_id: int, ano_edicao: int) -> Optional[Inscricao]:
        """Get inscricao by estudante ID and year."""
        return self.db.query(Inscricao).filter(
            Inscricao.estudante_id == estudante_id,
            Inscricao.ano_edicao == ano_edicao
        ).first()

