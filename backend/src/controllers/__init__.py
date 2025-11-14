"""Controller layer."""
from .escola_controller import router as escola_router
from .estudante_controller import router as estudante_router
from .inscricao_controller import router as inscricao_router
from .equipe_controller import router as equipe_router
from .equipe_membro_controller import router as equipe_membro_router

__all__ = [
    "escola_router",
    "estudante_router",
    "inscricao_router",
    "equipe_router",
    "equipe_membro_router",
]

