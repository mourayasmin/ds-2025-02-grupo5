"""DTOs (Data Transfer Objects)."""
from .escola_dto import EscolaCreate, EscolaUpdate, EscolaResponse
from .estudante_dto import EstudanteCreate, EstudanteUpdate, EstudanteResponse
from .inscricao_dto import InscricaoCreate, InscricaoUpdate, InscricaoResponse
from .equipe_dto import EquipeCreate, EquipeUpdate, EquipeResponse
from .equipe_membro_dto import EquipeMembroCreate, EquipeMembroUpdate, EquipeMembroResponse

__all__ = [
    "EscolaCreate",
    "EscolaUpdate",
    "EscolaResponse",
    "EstudanteCreate",
    "EstudanteUpdate",
    "EstudanteResponse",
    "InscricaoCreate",
    "InscricaoUpdate",
    "InscricaoResponse",
    "EquipeCreate",
    "EquipeUpdate",
    "EquipeResponse",
    "EquipeMembroCreate",
    "EquipeMembroUpdate",
    "EquipeMembroResponse",
]

