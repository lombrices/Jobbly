from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, database
from ..crud import petitioner_service_crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para crear un nuevo petitioner_service
@router.post("/petitioner_service", response_model=schemas.PetitionerService)
async def create_petitioner_service(
    petitioner_service: schemas.PetitionerServiceCreate,
    db: AsyncSession = Depends(get_db)
):
    # Llamamos a la función create_petitioner_service desde el CRUD
    db_petitioner_service = await petitioner_service_crud.create_petitioner_service(
        db=db, petitioner_service=petitioner_service
    )
    return db_petitioner_service


# Ruta para obtener registros de petitioner_service por id del trabajador
@router.get("/petitioner_service/worker/{worker_id}", response_model=List[schemas.PetitionerService])
async def get_petitioner_services_by_worker_id(
    worker_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene todos los registros de PetitionerService relacionados con un id_worker específico.
    """
    # Llamamos a la función get_petitioner_service_by_worker_id desde el CRUD
    petitioner_services = await petitioner_service_crud.get_petitioner_service_by_worker_id(
        db=db, worker_id=worker_id
    )
    # Validamos si se encontraron registros
    if not petitioner_services:
        raise HTTPException(status_code=404, detail="No services found for the specified worker")
    return petitioner_services

# Ruta para obtener registros resueltos de petitioner_service por id del trabajador
@router.get("/petitioner_service/worker/{worker_id}/resolved", response_model=List[schemas.PetitionerService])
async def get_resolved_petitioner_services_by_worker_id(
    worker_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene todos los registros resueltos de PetitionerService relacionados con un id_worker específico.
    """
    # Llamamos a la función get_resolved_petitioner_service_by_worker_id desde el CRUD
    resolved_petitioner_services = await petitioner_service_crud.get_resolved_petitioner_service_by_worker_id(
        db=db, worker_id=worker_id
    )
    # Validamos si se encontraron registros
    if not resolved_petitioner_services:
        raise HTTPException(status_code=404, detail="No resolved services found for the specified worker")
    return resolved_petitioner_services

# Ruta para obtener registros no resueltos de petitioner_service por id del trabajador
@router.get("/petitioner_service/worker/{worker_id}/unresolved", response_model=List[schemas.PetitionerService])
async def get_unresolved_petitioner_services_by_worker_id(
    worker_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene todos los registros no resueltos de PetitionerService relacionados con un id_worker específico.
    """
    # Llamamos a la función get_unresolved_petitioner_service_by_worker_id desde el CRUD
    unresolved_petitioner_services = await petitioner_service_crud.get_unresolved_petitioner_service_by_worker_id(
        db=db, worker_id=worker_id
    )
    # Validamos si se encontraron registros
    if not unresolved_petitioner_services:
        raise HTTPException(status_code=404, detail="No unresolved services found for the specified worker")
    return unresolved_petitioner_services

# Ruta para marcar un petitioner_service como resuelto
@router.put("/petitioner_service/{petitioner_service_id}/resolve", response_model=schemas.PetitionerService)
async def mark_petitioner_service_resolved(
    petitioner_service_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Marca un servicio de petitioner_service como resuelto (solved=True).
    """
    # Llamamos a la función para marcar como resuelto en el CRUD
    updated_petitioner_service = await petitioner_service_crud.mark_petitioner_service_as_resolved(
        db=db, petitioner_service_id=petitioner_service_id
    )
    
    return updated_petitioner_service
