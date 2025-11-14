"""Inscricao controller."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.services.inscricao_service import InscricaoService
from src.dto.inscricao_dto import InscricaoCreate, InscricaoUpdate, InscricaoResponse

router = APIRouter(prefix="/inscricoes", tags=["inscricoes"])


@router.post("/", response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
def create_inscricao(inscricao: InscricaoCreate, db: Session = Depends(get_db)):
    """Create a new inscricao."""
    service = InscricaoService(db)
    try:
        return service.create_inscricao(**inscricao.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[InscricaoResponse])
def get_inscricoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all inscricoes."""
    service = InscricaoService(db)
    return service.get_all_inscricoes(skip=skip, limit=limit)


@router.get("/{inscricao_id}", response_model=InscricaoResponse)
def get_inscricao(inscricao_id: int, db: Session = Depends(get_db)):
    """Get inscricao by ID."""
    service = InscricaoService(db)
    inscricao = service.get_inscricao_by_id(inscricao_id)
    if not inscricao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inscricao with ID {inscricao_id} not found"
        )
    return inscricao


@router.get("/estudante/{estudante_id}", response_model=List[InscricaoResponse])
def get_inscricoes_by_estudante(estudante_id: int, db: Session = Depends(get_db)):
    """Get inscricoes by estudante."""
    service = InscricaoService(db)
    return service.get_inscricoes_by_estudante(estudante_id)


@router.get("/escola/{escola_id}", response_model=List[InscricaoResponse])
def get_inscricoes_by_escola(escola_id: int, db: Session = Depends(get_db)):
    """Get inscricoes by escola."""
    service = InscricaoService(db)
    return service.get_inscricoes_by_escola(escola_id)


@router.get("/ano/{ano_edicao}", response_model=List[InscricaoResponse])
def get_inscricoes_by_ano(ano_edicao: int, db: Session = Depends(get_db)):
    """Get inscricoes by year."""
    service = InscricaoService(db)
    return service.get_inscricoes_by_ano(ano_edicao)


@router.get("/status/{status}", response_model=List[InscricaoResponse])
def get_inscricoes_by_status(status: str, db: Session = Depends(get_db)):
    """Get inscricoes by status."""
    service = InscricaoService(db)
    return service.get_inscricoes_by_status(status)


@router.put("/{inscricao_id}", response_model=InscricaoResponse)
def update_inscricao(
    inscricao_id: int,
    inscricao: InscricaoUpdate,
    db: Session = Depends(get_db)
):
    """Update inscricao."""
    service = InscricaoService(db)
    updated = service.update_inscricao(inscricao_id, **inscricao.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inscricao with ID {inscricao_id} not found"
        )
    return updated


@router.post("/{inscricao_id}/confirmar", response_model=InscricaoResponse)
def confirm_inscricao(inscricao_id: int, db: Session = Depends(get_db)):
    """Confirm an inscricao."""
    service = InscricaoService(db)
    inscricao = service.confirm_inscricao(inscricao_id)
    if not inscricao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inscricao with ID {inscricao_id} not found"
        )
    return inscricao


@router.post("/{inscricao_id}/cancelar", response_model=InscricaoResponse)
def cancel_inscricao(inscricao_id: int, db: Session = Depends(get_db)):
    """Cancel an inscricao."""
    service = InscricaoService(db)
    inscricao = service.cancel_inscricao(inscricao_id)
    if not inscricao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inscricao with ID {inscricao_id} not found"
        )
    return inscricao


@router.delete("/{inscricao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inscricao(inscricao_id: int, db: Session = Depends(get_db)):
    """Delete inscricao."""
    service = InscricaoService(db)
    if not service.delete_inscricao(inscricao_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inscricao with ID {inscricao_id} not found"
        )

