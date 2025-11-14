"""Equipe controller."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.services.equipe_service import EquipeService
from src.dto.equipe_dto import EquipeCreate, EquipeUpdate, EquipeResponse

router = APIRouter(prefix="/equipes", tags=["equipes"])


@router.post("/", response_model=EquipeResponse, status_code=status.HTTP_201_CREATED)
def create_equipe(equipe: EquipeCreate, db: Session = Depends(get_db)):
    """Create a new equipe."""
    service = EquipeService(db)
    try:
        return service.create_equipe(**equipe.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[EquipeResponse])
def get_equipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all equipes."""
    service = EquipeService(db)
    return service.get_all_equipes(skip=skip, limit=limit)


@router.get("/{equipe_id}", response_model=EquipeResponse)
def get_equipe(equipe_id: int, db: Session = Depends(get_db)):
    """Get equipe by ID."""
    service = EquipeService(db)
    equipe = service.get_equipe_by_id(equipe_id)
    if not equipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipe with ID {equipe_id} not found"
        )
    return equipe


@router.get("/escola/{escola_id}", response_model=List[EquipeResponse])
def get_equipes_by_escola(escola_id: int, db: Session = Depends(get_db)):
    """Get equipes by escola."""
    service = EquipeService(db)
    return service.get_equipes_by_escola(escola_id)


@router.get("/ano/{ano_edicao}", response_model=List[EquipeResponse])
def get_equipes_by_ano(ano_edicao: int, db: Session = Depends(get_db)):
    """Get equipes by year."""
    service = EquipeService(db)
    return service.get_equipes_by_ano(ano_edicao)


@router.get("/status/{status}", response_model=List[EquipeResponse])
def get_equipes_by_status(status: str, db: Session = Depends(get_db)):
    """Get equipes by status."""
    service = EquipeService(db)
    return service.get_equipes_by_status(status)


@router.put("/{equipe_id}", response_model=EquipeResponse)
def update_equipe(
    equipe_id: int,
    equipe: EquipeUpdate,
    db: Session = Depends(get_db)
):
    """Update equipe."""
    service = EquipeService(db)
    try:
        updated = service.update_equipe(equipe_id, **equipe.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipe with ID {equipe_id} not found"
            )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{equipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_equipe(equipe_id: int, db: Session = Depends(get_db)):
    """Delete equipe."""
    service = EquipeService(db)
    if not service.delete_equipe(equipe_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipe with ID {equipe_id} not found"
        )

