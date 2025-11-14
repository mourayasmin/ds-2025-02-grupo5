"""Escola service."""
from typing import List, Optional
from sqlalchemy.orm import Session
from src.entities.escola import Escola
from src.repositories.escola_repository import EscolaRepository


class EscolaService:
    """Service for Escola business logic."""

    def __init__(self, db: Session):
        self.repository = EscolaRepository(db)

    def create_escola(
        self,
        nome: str,
        cidade: str,
        estado: str = "GO",
        endereco: Optional[str] = None,
        cep: Optional[str] = None,
        telefone: Optional[str] = None,
        email: Optional[str] = None,
        diretor_nome: Optional[str] = None,
        ativo: bool = True,
    ) -> Escola:
        """Create a new escola."""
        # Check if escola with same name already exists
        existing = self.repository.get_by_nome(nome)
        if existing:
            raise ValueError(f"Escola with name '{nome}' already exists")

        return self.repository.create(
            nome=nome,
            cidade=cidade,
            estado=estado,
            endereco=endereco,
            cep=cep,
            telefone=telefone,
            email=email,
            diretor_nome=diretor_nome,
            ativo=ativo,
        )

    def get_escola_by_id(self, escola_id: int) -> Optional[Escola]:
        """Get escola by ID."""
        return self.repository.get_by_id(escola_id)

    def get_all_escolas(self, skip: int = 0, limit: int = 100) -> List[Escola]:
        """Get all escolas."""
        return self.repository.get_all(skip=skip, limit=limit)

    def get_escolas_by_cidade(self, cidade: str) -> List[Escola]:
        """Get escolas by city."""
        return self.repository.get_by_cidade(cidade)

    def get_active_escolas(self) -> List[Escola]:
        """Get all active escolas."""
        return self.repository.get_active()

    def update_escola(self, escola_id: int, **kwargs) -> Optional[Escola]:
        """Update escola."""
        return self.repository.update(escola_id, **kwargs)

    def delete_escola(self, escola_id: int) -> bool:
        """Delete escola."""
        return self.repository.delete(escola_id)

