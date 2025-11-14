"""EquipeMembro controller."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.services.equipe_membro_service import EquipeMembroService
from src.dto.equipe_membro_dto import EquipeMembroCreate, EquipeMembroUpdate, EquipeMembroResponse

router = APIRouter(prefix="/equipe-membros", tags=["equipe-membros"])


@router.post("/", response_model=EquipeMembroResponse, status_code=status.HTTP_201_CREATED)
def create_equipe_membro(membro: EquipeMembroCreate, db: Session = Depends(get_db)):
    """Add estudante to equipe."""
    service = EquipeMembroService(db)
    try:
        return service.create_equipe_membro(**membro.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[EquipeMembroResponse])
def get_equipe_membros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all equipe membros."""
    service = EquipeMembroService(db)
    return service.repository.get_all(skip=skip, limit=limit)


@router.get("/{membro_id}", response_model=EquipeMembroResponse)
def get_equipe_membro(membro_id: int, db: Session = Depends(get_db)):
    """Get equipe membro by ID."""
    service = EquipeMembroService(db)
    membro = service.get_equipe_membro_by_id(membro_id)
    if not membro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipe membro with ID {membro_id} not found"
        )
    return membro


@router.get("/equipe/{equipe_id}", response_model=List[EquipeMembroResponse])
def get_membros_by_equipe(equipe_id: int, db: Session = Depends(get_db)):
    """Get all membros of an equipe."""
    service = EquipeMembroService(db)
    return service.get_membros_by_equipe(equipe_id)


@router.get("/estudante/{estudante_id}", response_model=List[EquipeMembroResponse])
def get_equipes_by_estudante(estudante_id: int, db: Session = Depends(get_db)):
    """Get all equipes that an estudante belongs to."""
    service = EquipeMembroService(db)
    return service.get_equipes_by_estudante(estudante_id)


@router.put("/{membro_id}", response_model=EquipeMembroResponse)
def update_equipe_membro(
    membro_id: int,
    membro: EquipeMembroUpdate,
    db: Session = Depends(get_db)
):
    """Update equipe membro."""
    service = EquipeMembroService(db)
    updated = service.update_equipe_membro(membro_id, **membro.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipe membro with ID {membro_id} not found"
        )
    return updated


@router.delete("/equipe/{equipe_id}/estudante/{estudante_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_estudante_from_equipe(equipe_id: int, estudante_id: int, db: Session = Depends(get_db)):
    """Remove estudante from equipe."""
    service = EquipeMembroService(db)
    if not service.remove_estudante_from_equipe(equipe_id, estudante_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estudante {estudante_id} is not a member of equipe {equipe_id}"
        )


@router.delete("/{membro_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_equipe_membro(membro_id: int, db: Session = Depends(get_db)):
    """Delete equipe membro."""
    service = EquipeMembroService(db)
    if not service.delete_equipe_membro(membro_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipe membro with ID {membro_id} not found"
        )

