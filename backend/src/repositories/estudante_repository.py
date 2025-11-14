"""Estudante repository."""
from typing import Optional, List
from sqlalchemy.orm import Session
from src.entities.estudante import Estudante
from .base_repository import BaseRepository


class EstudanteRepository(BaseRepository[Estudante]):
    """Repository for Estudante entity."""

    def __init__(self, db: Session):
        super().__init__(Estudante, db)

    def get_by_cpf(self, cpf: str) -> Optional[Estudante]:
        """Get estudante by CPF."""
        return self.db.query(Estudante).filter(Estudante.cpf == cpf).first()

    def get_by_escola_id(self, escola_id: int) -> List[Estudante]:
        """Get estudantes by escola ID."""
        return self.db.query(Estudante).filter(Estudante.escola_id == escola_id).all()

    def get_by_email(self, email: str) -> Optional[Estudante]:
        """Get estudante by email."""
        return self.db.query(Estudante).filter(Estudante.email == email).first()

