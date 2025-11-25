"""Escola repository."""
from typing import Optional, List
from sqlalchemy.orm import Session
from src.entities.escola import Escola
from .base_repository import BaseRepository


class EscolaRepository(BaseRepository[Escola]):
    """Repository for Escola entity."""

    def __init__(self, db: Session):
        super().__init__(Escola, db)

    def get_by_nome(self, nome: str) -> Optional[Escola]:
        """Get escola by name."""
        return self.db.query(Escola).filter(Escola.nome == nome).first()

    def get_by_cidade(self, cidade: str) -> List[Escola]:
        """Get escolas by city."""
        return self.db.query(Escola).filter(Escola.cidade == cidade).all()

    def get_active(self) -> List[Escola]:
        """Get all active escolas."""
        return self.db.query(Escola).filter(Escola.ativo == True).all()
    
    def search_by_name(self, nome: str) -> List[Escola]:
        """Search escolas by name."""
        return self.db.query(Escola).filter(Escola.nome.ilike(f"%{nome}%")).all()