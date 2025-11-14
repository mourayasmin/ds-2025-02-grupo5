"""Estudante service."""
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from src.entities.estudante import Estudante
from src.repositories.estudante_repository import EstudanteRepository
from src.repositories.escola_repository import EscolaRepository


class EstudanteService:
    """Service for Estudante business logic."""

    def __init__(self, db: Session):
        self.repository = EstudanteRepository(db)
        self.escola_repository = EscolaRepository(db)

    def create_estudante(
        self,
        nome_completo: str,
        cpf: str,
        data_nascimento: date,
        email: str,
        escola_id: int,
        serie_ano: str,
        telefone: Optional[str] = None,
        turno: Optional[str] = None,
    ) -> Estudante:
        """Create a new estudante."""
        # Validate escola exists
        escola = self.escola_repository.get_by_id(escola_id)
        if not escola:
            raise ValueError(f"Escola with ID {escola_id} not found")

        if not escola.ativo:
            raise ValueError(f"Escola with ID {escola_id} is not active")

        # Check if CPF already exists
        existing = self.repository.get_by_cpf(cpf)
        if existing:
            raise ValueError(f"Estudante with CPF '{cpf}' already exists")

        # Check if email already exists
        existing_email = self.repository.get_by_email(email)
        if existing_email:
            raise ValueError(f"Estudante with email '{email}' already exists")

        return self.repository.create(
            nome_completo=nome_completo,
            cpf=cpf,
            data_nascimento=data_nascimento,
            email=email,
            escola_id=escola_id,
            serie_ano=serie_ano,
            telefone=telefone,
            turno=turno,
        )

    def get_estudante_by_id(self, estudante_id: int) -> Optional[Estudante]:
        """Get estudante by ID."""
        return self.repository.get_by_id(estudante_id)

    def get_estudante_by_cpf(self, cpf: str) -> Optional[Estudante]:
        """Get estudante by CPF."""
        return self.repository.get_by_cpf(cpf)

    def get_all_estudantes(self, skip: int = 0, limit: int = 100) -> List[Estudante]:
        """Get all estudantes."""
        return self.repository.get_all(skip=skip, limit=limit)

    def get_estudantes_by_escola(self, escola_id: int) -> List[Estudante]:
        """Get estudantes by escola."""
        return self.repository.get_by_escola_id(escola_id)

    def update_estudante(self, estudante_id: int, **kwargs) -> Optional[Estudante]:
        """Update estudante."""
        # If updating escola_id, validate it exists
        if "escola_id" in kwargs:
            escola = self.escola_repository.get_by_id(kwargs["escola_id"])
            if not escola:
                raise ValueError(f"Escola with ID {kwargs['escola_id']} not found")
            if not escola.ativo:
                raise ValueError(f"Escola with ID {kwargs['escola_id']} is not active")

        return self.repository.update(estudante_id, **kwargs)

    def delete_estudante(self, estudante_id: int) -> bool:
        """Delete estudante."""
        return self.repository.delete(estudante_id)

