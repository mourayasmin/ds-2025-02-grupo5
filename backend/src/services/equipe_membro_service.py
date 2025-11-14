"""EquipeMembro service."""
from typing import List, Optional
from sqlalchemy.orm import Session
from src.entities.equipe_membro import EquipeMembro
from src.repositories.equipe_membro_repository import EquipeMembroRepository
from src.repositories.equipe_repository import EquipeRepository
from src.repositories.estudante_repository import EstudanteRepository


class EquipeMembroService:
    """Service for EquipeMembro business logic."""

    def __init__(self, db: Session):
        self.repository = EquipeMembroRepository(db)
        self.equipe_repository = EquipeRepository(db)
        self.estudante_repository = EstudanteRepository(db)

    def create_equipe_membro(
        self,
        equipe_id: int,
        estudante_id: int,
        papel: str = "membro",
    ) -> EquipeMembro:
        """Add estudante to equipe."""
        # Validate equipe exists
        equipe = self.equipe_repository.get_by_id(equipe_id)
        if not equipe:
            raise ValueError(f"Equipe with ID {equipe_id} not found")

        # Validate estudante exists
        estudante = self.estudante_repository.get_by_id(estudante_id)
        if not estudante:
            raise ValueError(f"Estudante with ID {estudante_id} not found")

        # Validate estudante belongs to same escola as equipe
        if estudante.escola_id != equipe.escola_id:
            raise ValueError(f"Estudante must belong to same escola as equipe")

        # Check if membro already exists
        existing = self.repository.get_by_equipe_and_estudante(equipe_id, estudante_id)
        if existing:
            raise ValueError(f"Estudante {estudante_id} is already a member of equipe {equipe_id}")

        return self.repository.create(
            equipe_id=equipe_id,
            estudante_id=estudante_id,
            papel=papel,
        )

    def get_equipe_membro_by_id(self, membro_id: int) -> Optional[EquipeMembro]:
        """Get equipe membro by ID."""
        return self.repository.get_by_id(membro_id)

    def get_membros_by_equipe(self, equipe_id: int) -> List[EquipeMembro]:
        """Get all membros of an equipe."""
        return self.repository.get_by_equipe_id(equipe_id)

    def get_equipes_by_estudante(self, estudante_id: int) -> List[EquipeMembro]:
        """Get all equipes that an estudante belongs to."""
        return self.repository.get_by_estudante_id(estudante_id)

    def update_equipe_membro(self, membro_id: int, **kwargs) -> Optional[EquipeMembro]:
        """Update equipe membro."""
        return self.repository.update(membro_id, **kwargs)

    def remove_estudante_from_equipe(self, equipe_id: int, estudante_id: int) -> bool:
        """Remove estudante from equipe."""
        membro = self.repository.get_by_equipe_and_estudante(equipe_id, estudante_id)
        if membro:
            return self.repository.delete(membro.id)
        return False

    def delete_equipe_membro(self, membro_id: int) -> bool:
        """Delete equipe membro."""
        return self.repository.delete(membro_id)

