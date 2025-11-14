"""Escola controller."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.services.escola_service import EscolaService
from src.dto.escola_dto import EscolaCreate, EscolaUpdate, EscolaResponse

router = APIRouter(prefix="/escolas", tags=["escolas"])


@router.post("/", response_model=EscolaResponse, status_code=status.HTTP_201_CREATED)
def create_escola(escola: EscolaCreate, db: Session = Depends(get_db)):
    """Create a new escola."""
    service = EscolaService(db)
    try:
        return service.create_escola(**escola.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[EscolaResponse])
def get_escolas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all escolas."""
    service = EscolaService(db)
    return service.get_all_escolas(skip=skip, limit=limit)


@router.get("/{escola_id}", response_model=EscolaResponse)
def get_escola(escola_id: int, db: Session = Depends(get_db)):
    """Get escola by ID."""
    service = EscolaService(db)
    escola = service.get_escola_by_id(escola_id)
    if not escola:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Escola with ID {escola_id} not found"
        )
    return escola


@router.get("/cidade/{cidade}", response_model=List[EscolaResponse])
def get_escolas_by_cidade(cidade: str, db: Session = Depends(get_db)):
    """Get escolas by city."""
    service = EscolaService(db)
    return service.get_escolas_by_cidade(cidade)


@router.get("/status/active", response_model=List[EscolaResponse])
def get_active_escolas(db: Session = Depends(get_db)):
    """Get all active escolas."""
    service = EscolaService(db)
    return service.get_active_escolas()


@router.put("/{escola_id}", response_model=EscolaResponse)
def update_escola(
    escola_id: int,
    escola: EscolaUpdate,
    db: Session = Depends(get_db)
):
    """Update escola."""
    service = EscolaService(db)
    updated = service.update_escola(escola_id, **escola.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Escola with ID {escola_id} not found"
        )
    return updated


@router.delete("/{escola_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_escola(escola_id: int, db: Session = Depends(get_db)):
    """Delete escola."""
    service = EscolaService(db)
    if not service.delete_escola(escola_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Escola with ID {escola_id} not found"
        )

