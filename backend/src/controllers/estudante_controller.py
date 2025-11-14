"""Estudante controller."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.services.estudante_service import EstudanteService
from src.dto.estudante_dto import EstudanteCreate, EstudanteUpdate, EstudanteResponse

router = APIRouter(prefix="/estudantes", tags=["estudantes"])


@router.post("/", response_model=EstudanteResponse, status_code=status.HTTP_201_CREATED)
def create_estudante(estudante: EstudanteCreate, db: Session = Depends(get_db)):
    """Create a new estudante."""
    service = EstudanteService(db)
    try:
        return service.create_estudante(**estudante.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[EstudanteResponse])
def get_estudantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all estudantes."""
    service = EstudanteService(db)
    return service.get_all_estudantes(skip=skip, limit=limit)


@router.get("/{estudante_id}", response_model=EstudanteResponse)
def get_estudante(estudante_id: int, db: Session = Depends(get_db)):
    """Get estudante by ID."""
    service = EstudanteService(db)
    estudante = service.get_estudante_by_id(estudante_id)
    if not estudante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estudante with ID {estudante_id} not found"
        )
    return estudante


@router.get("/cpf/{cpf}", response_model=EstudanteResponse)
def get_estudante_by_cpf(cpf: str, db: Session = Depends(get_db)):
    """Get estudante by CPF."""
    service = EstudanteService(db)
    estudante = service.get_estudante_by_cpf(cpf)
    if not estudante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estudante with CPF {cpf} not found"
        )
    return estudante


@router.get("/escola/{escola_id}", response_model=List[EstudanteResponse])
def get_estudantes_by_escola(escola_id: int, db: Session = Depends(get_db)):
    """Get estudantes by escola."""
    service = EstudanteService(db)
    return service.get_estudantes_by_escola(escola_id)


@router.put("/{estudante_id}", response_model=EstudanteResponse)
def update_estudante(
    estudante_id: int,
    estudante: EstudanteUpdate,
    db: Session = Depends(get_db)
):
    """Update estudante."""
    service = EstudanteService(db)
    try:
        updated = service.update_estudante(estudante_id, **estudante.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudante with ID {estudante_id} not found"
            )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{estudante_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_estudante(estudante_id: int, db: Session = Depends(get_db)):
    """Delete estudante."""
    service = EstudanteService(db)
    if not service.delete_estudante(estudante_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estudante with ID {estudante_id} not found"
        )

