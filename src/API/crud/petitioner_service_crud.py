from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from .. import models, schemas, database
from datetime import datetime
from typing import List


# Crear un nuevo registro de petitioner_service
async def create_petitioner_service(
    db: AsyncSession,
    petitioner_service: schemas.PetitionerServiceCreate
):
    db_petitioner_service = models.PetitionerService(**petitioner_service.dict())
    # Añadir la instancia a la sesión de base de datos
    db.add(db_petitioner_service)
    # Confirmar los cambios en la base de datos
    await db.commit()
    # Refrescar el objeto para obtener el ID generado
    await db.refresh(db_petitioner_service)

    return db_petitioner_service

# Obtener registros de petitioner_service por id del trabajador
async def get_petitioner_service_by_worker_id(
    db: AsyncSession, 
    worker_id: int
) -> List[schemas.PetitionerService]:
    """
    Obtiene todos los registros de PetitionerService relacionados con un id_worker específico.
    """
    query = (
        select(models.PetitionerService)
        .join(models.Service, models.Service.id == models.PetitionerService.id_service)
        .where(models.Service.id_worker == worker_id)
        .options(
            joinedload(models.PetitionerService.service),  # Carga el servicio relacionado
            joinedload(models.PetitionerService.petitioner)  # Carga el peticionario relacionado
        )
    )
    
    result = await db.execute(query)
    # Recuperar los registros como una lista
    petitioner_services = result.scalars().all()
    return petitioner_services

# Obtener registros resueltos de petitioner_service por id del trabajador
async def get_resolved_petitioner_service_by_worker_id(
    db: AsyncSession, 
    worker_id: int
) -> List[schemas.PetitionerService]:
    """
    Obtiene todos los registros de PetitionerService relacionados con un id_worker específico
    donde el servicio está marcado como resuelto (solved=True).
    """
    query = (
        select(models.PetitionerService)
        .join(models.Service, models.Service.id == models.PetitionerService.id_service)
        .where(models.Service.id_worker == worker_id)
        .where(models.PetitionerService.solved == True)  # Filtra por los registros resueltos
        .options(
            joinedload(models.PetitionerService.service),  # Carga el servicio relacionado
            joinedload(models.PetitionerService.petitioner)  # Carga el peticionario relacionado
        )
    )
    
    result = await db.execute(query)
    # Recuperar los registros como una lista
    resolved_petitioner_services = result.scalars().all()
    return resolved_petitioner_services

# Obtener registros no resueltos de petitioner_service por id del trabajador
async def get_unresolved_petitioner_service_by_worker_id(
    db: AsyncSession, 
    worker_id: int
) -> List[schemas.PetitionerService]:
    """
    Obtiene todos los registros de PetitionerService relacionados con un id_worker específico
    donde el servicio está marcado como no resuelto (solved=False).
    """
    query = (
        select(models.PetitionerService)
        .join(models.Service, models.Service.id == models.PetitionerService.id_service)
        .where(models.Service.id_worker == worker_id)
        .where(models.PetitionerService.solved == False)  # Filtra por los registros no resueltos
        .options(
            joinedload(models.PetitionerService.service),  # Carga el servicio relacionado
            joinedload(models.PetitionerService.petitioner)  # Carga el peticionario relacionado
        )
    )
    
    result = await db.execute(query)
    # Recuperar los registros como una lista
    unresolved_petitioner_services = result.scalars().all()
    return unresolved_petitioner_services

# Marcar un petitioner_service como resuelto
async def mark_petitioner_service_as_resolved(
    db: AsyncSession, 
    petitioner_service_id: int
) -> models.PetitionerService:
    """
    Marca un servicio de petitioner_service como resuelto (solved=True).
    """
    # Buscar el registro PetitionerService por su ID
    petitioner_service = await db.get(models.PetitionerService, petitioner_service_id)
    
    if not petitioner_service:
        raise HTTPException(status_code=404, detail="PetitionerService not found")
    
    # Actualizar el estado a resuelto
    petitioner_service.solved = True
    await db.commit()
    await db.refresh(petitioner_service)
    
    return petitioner_service
