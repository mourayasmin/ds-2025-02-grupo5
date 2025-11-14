"""Inscricao service."""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from src.entities.inscricao import Inscricao
from src.repositories.inscricao_repository import InscricaoRepository
from src.repositories.estudante_repository import EstudanteRepository
from src.repositories.escola_repository import EscolaRepository


class InscricaoService:
    """Service for Inscricao business logic."""

    def __init__(self, db: Session):
        self.repository = InscricaoRepository(db)
        self.estudante_repository = EstudanteRepository(db)
        self.escola_repository = EscolaRepository(db)

    def create_inscricao(
        self,
        estudante_id: int,
        escola_id: int,
        ano_edicao: int,
        categoria: Optional[str] = None,
        equipe_nome: Optional[str] = None,
        observacoes: Optional[str] = None,
    ) -> Inscricao:
        """Create a new inscricao."""
        # Validate estudante exists
        estudante = self.estudante_repository.get_by_id(estudante_id)
        if not estudante:
            raise ValueError(f"Estudante with ID {estudante_id} not found")

        # Validate escola exists
        escola = self.escola_repository.get_by_id(escola_id)
        if not escola:
            raise ValueError(f"Escola with ID {escola_id} not found")

        # Validate estudante belongs to escola
        if estudante.escola_id != escola_id:
            raise ValueError(f"Estudante does not belong to escola {escola_id}")

        # Check if inscricao already exists for this estudante and year
        existing = self.repository.get_by_estudante_and_ano(estudante_id, ano_edicao)
        if existing:
            raise ValueError(f"Inscricao already exists for estudante {estudante_id} in year {ano_edicao}")

        return self.repository.create(
            estudante_id=estudante_id,
            escola_id=escola_id,
            ano_edicao=ano_edicao,
            status="pendente",
            categoria=categoria,
            equipe_nome=equipe_nome,
            observacoes=observacoes,
            data_inscricao=datetime.utcnow(),
        )

    def get_inscricao_by_id(self, inscricao_id: int) -> Optional[Inscricao]:
        """Get inscricao by ID."""
        return self.repository.get_by_id(inscricao_id)

    def get_all_inscricoes(self, skip: int = 0, limit: int = 100) -> List[Inscricao]:
        """Get all inscricoes."""
        return self.repository.get_all(skip=skip, limit=limit)

    def get_inscricoes_by_estudante(self, estudante_id: int) -> List[Inscricao]:
        """Get inscricoes by estudante."""
        return self.repository.get_by_estudante_id(estudante_id)

    def get_inscricoes_by_escola(self, escola_id: int) -> List[Inscricao]:
        """Get inscricoes by escola."""
        return self.repository.get_by_escola_id(escola_id)

    def get_inscricoes_by_ano(self, ano_edicao: int) -> List[Inscricao]:
        """Get inscricoes by year."""
        return self.repository.get_by_ano_edicao(ano_edicao)

    def get_inscricoes_by_status(self, status: str) -> List[Inscricao]:
        """Get inscricoes by status."""
        return self.repository.get_by_status(status)

    def update_inscricao(self, inscricao_id: int, **kwargs) -> Optional[Inscricao]:
        """Update inscricao."""
        return self.repository.update(inscricao_id, **kwargs)

    def confirm_inscricao(self, inscricao_id: int) -> Optional[Inscricao]:
        """Confirm an inscricao."""
        return self.repository.update(
            inscricao_id,
            status="confirmada",
            data_confirmacao=datetime.utcnow(),
        )

    def cancel_inscricao(self, inscricao_id: int) -> Optional[Inscricao]:
        """Cancel an inscricao."""
        return self.repository.update(inscricao_id, status="cancelada")

    def delete_inscricao(self, inscricao_id: int) -> bool:
        """Delete inscricao."""
        return self.repository.delete(inscricao_id)

