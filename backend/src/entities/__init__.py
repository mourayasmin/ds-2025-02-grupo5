"""Entity models."""
from .escola import Escola
from .estudante import Estudante
from .inscricao import Inscricao
from .equipe import Equipe
from .equipe_membro import EquipeMembro

__all__ = [
    "Escola",
    "Estudante",
    "Inscricao",
    "Equipe",
    "EquipeMembro",
]

