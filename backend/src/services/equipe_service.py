"""Equipe service."""
from typing import List, Optional
from sqlalchemy.orm import Session
from src.entities.equipe import Equipe
from src.repositories.equipe_repository import EquipeRepository
from src.repositories.escola_repository import EscolaRepository
from src.repositories.estudante_repository import EstudanteRepository


class EquipeService:
    """Service for Equipe business logic."""

    def __init__(self, db: Session):
        self.repository = EquipeRepository(db)
        self.escola_repository = EscolaRepository(db)
        self.estudante_repository = EstudanteRepository(db)

    def create_equipe(
        self,
        nome: str,
        escola_id: int,
        ano_edicao: int,
        categoria: Optional[str] = None,
        lider_id: Optional[int] = None,
        status: str = "formando",
    ) -> Equipe:
        """Create a new equipe."""
        # Validate escola exists
        escola = self.escola_repository.get_by_id(escola_id)
        if not escola:
            raise ValueError(f"Escola with ID {escola_id} not found")

        # Validate lider if provided
        if lider_id:
            lider = self.estudante_repository.get_by_id(lider_id)
            if not lider:
                raise ValueError(f"Estudante (lider) with ID {lider_id} not found")
            if lider.escola_id != escola_id:
                raise ValueError(f"Lider must belong to escola {escola_id}")

        return self.repository.create(
            nome=nome,
            escola_id=escola_id,
            ano_edicao=ano_edicao,
            categoria=categoria,
            lider_id=lider_id,
            status=status,
        )

    def get_equipe_by_id(self, equipe_id: int) -> Optional[Equipe]:
        """Get equipe by ID."""
        return self.repository.get_by_id(equipe_id)

    def get_all_equipes(self, skip: int = 0, limit: int = 100) -> List[Equipe]:
        """Get all equipes."""
        return self.repository.get_all(skip=skip, limit=limit)

    def get_equipes_by_escola(self, escola_id: int) -> List[Equipe]:
        """Get equipes by escola."""
        return self.repository.get_by_escola_id(escola_id)

    def get_equipes_by_ano(self, ano_edicao: int) -> List[Equipe]:
        """Get equipes by year."""
        return self.repository.get_by_ano_edicao(ano_edicao)

    def get_equipes_by_status(self, status: str) -> List[Equipe]:
        """Get equipes by status."""
        return self.repository.get_by_status(status)

    def update_equipe(self, equipe_id: int, **kwargs) -> Optional[Equipe]:
        """Update equipe."""
        # Validate escola if updating
        if "escola_id" in kwargs:
            escola = self.escola_repository.get_by_id(kwargs["escola_id"])
            if not escola:
                raise ValueError(f"Escola with ID {kwargs['escola_id']} not found")

        # Validate lider if updating
        if "lider_id" in kwargs and kwargs["lider_id"]:
            lider = self.estudante_repository.get_by_id(kwargs["lider_id"])
            if not lider:
                raise ValueError(f"Estudante (lider) with ID {kwargs['lider_id']} not found")

        return self.repository.update(equipe_id, **kwargs)

    def delete_equipe(self, equipe_id: int) -> bool:
        """Delete equipe."""
        return self.repository.delete(equipe_id)

