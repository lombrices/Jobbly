from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, database
from ..crud import worker_request_crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para crear un nuevo worker_request
@router.post("/worker_request", response_model=schemas.WorkerRequest)
async def create_worker_request(
    worker_request: schemas.WorkerRequestCreate,
    db: AsyncSession = Depends(get_db)
):
    # Llamamos a la función create_worker_request desde el CRUD
    db_worker_request = await worker_request_crud.create_worker_request(
        db=db, worker_request=worker_request
    )
    return db_worker_request

# Ruta para obtener registros de worker_request por id del petitioner
@router.get("/worker_request/petitioner/{petitioner_id}", response_model=List[schemas.WorkerRequest])
async def get_worker_requests_by_petitioner_id(
    petitioner_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene todos los registros de WorkerRequest relacionados con un id_petitioner específico.
    """
    worker_requests = await worker_request_crud.get_worker_request_by_petitioner_id(
        db=db, petitioner_id=petitioner_id
    )
    
    # Validamos si se encontraron registros
    if not worker_requests:
        raise HTTPException(status_code=404, detail="No worker requests found for the specified petitioner")
    
    return worker_requests

# Ruta para obtener registros resueltos de worker_request por id del petitioner
@router.get("/worker_request/petitioner/{petitioner_id}/resolved", response_model=List[schemas.WorkerRequest])
async def get_resolved_worker_requests_by_petitioner_id(
    petitioner_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene los registros resueltos de WorkerRequest relacionados con un id_petitioner específico.
    """
    resolved_worker_requests = await worker_request_crud.get_resolved_worker_request_by_petitioner_id(
        db=db, petitioner_id=petitioner_id
    )
    
    # Validamos si se encontraron registros
    if not resolved_worker_requests:
        raise HTTPException(status_code=404, detail="No resolved worker requests found for the specified petitioner")
    
    return resolved_worker_requests

# Ruta para obtener registros no resueltos de worker_request por id del petitioner
@router.get("/worker_request/petitioner/{petitioner_id}/unresolved", response_model=List[schemas.WorkerRequest])
async def get_unresolved_worker_requests_by_petitioner_id(
    petitioner_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene los registros no resueltos de WorkerRequest relacionados con un id_petitioner específico.
    """
    unresolved_worker_requests = await worker_request_crud.get_unresolved_worker_request_by_petitioner_id(
        db=db, petitioner_id=petitioner_id
    )
    
    # Validamos si se encontraron registros
    if not unresolved_worker_requests:
        raise HTTPException(status_code=404, detail="No unresolved worker requests found for the specified petitioner")
    
    return unresolved_worker_requests

# Ruta para marcar un worker_request como resuelto
@router.put("/worker_request/{worker_request_id}/resolve", response_model=schemas.WorkerRequest)
async def mark_worker_request_resolved(
    worker_request_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Marca un worker_request como resuelto (solved=True).
    """
    updated_worker_request = await worker_request_crud.mark_worker_request_as_resolved(
        db=db, worker_request_id=worker_request_id
    )
    
    return updated_worker_request


