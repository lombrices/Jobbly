from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import models, schemas, database
from datetime import datetime

# Crear un nuevo registro de worker_request
async def create_worker_request(
    db: AsyncSession,
    worker_request: schemas.WorkerRequestCreate
):
    # Crear una instancia del modelo WorkerRequest
    db_worker_request = models.WorkerRequest(
        id_worker=worker_request.id_worker,
        id_request=worker_request.id_request,
        petition_date=worker_request.petition_date,
        solved=worker_request.solved
    )

    # Añadir la instancia a la sesión de base de datos
    db.add(db_worker_request)
    # Confirmar los cambios en la base de datos
    await db.commit()
    # Refrescar el objeto para obtener el ID generado
    await db.refresh(db_worker_request)

    return db_worker_request


# Obtener registros de worker_request por id del petitioner
async def get_worker_request_by_petitioner_id(
    db: AsyncSession, 
    petitioner_id: int
) -> list[models.WorkerRequest]:
    """
    Obtiene todos los registros de WorkerRequest relacionados con un id_petitioner específico.
    """
    query = (
        select(models.WorkerRequest)
        .join(models.Request, models.Request.id == models.WorkerRequest.id_request)
        .where(models.Request.id_petitioner == petitioner_id)
    )
    
    result = await db.execute(query)
    worker_requests = result.scalars().all()
    return worker_requests

# Obtener registros resueltos de worker_request por id del petitioner
async def get_resolved_worker_request_by_petitioner_id(
    db: AsyncSession, 
    petitioner_id: int
) -> list[models.WorkerRequest]:
    """
    Obtiene los registros resueltos de WorkerRequest relacionados con un id_petitioner específico.
    """
    query = (
        select(models.WorkerRequest)
        .join(models.Request, models.Request.id == models.WorkerRequest.id_request)
        .where(models.Request.id_petitioner == petitioner_id)
        .where(models.WorkerRequest.solved == True)
    )
    
    result = await db.execute(query)
    resolved_worker_requests = result.scalars().all()
    return resolved_worker_requests

# Obtener registros no resueltos de worker_request por id del petitioner
async def get_unresolved_worker_request_by_petitioner_id(
    db: AsyncSession, 
    petitioner_id: int
) -> list[models.WorkerRequest]:
    """
    Obtiene los registros no resueltos de WorkerRequest relacionados con un id_petitioner específico.
    """
    query = (
        select(models.WorkerRequest)
        .join(models.Request, models.Request.id == models.WorkerRequest.id_request)
        .where(models.Request.id_petitioner == petitioner_id)
        .where(models.WorkerRequest.solved == False)
    )
    
    result = await db.execute(query)
    unresolved_worker_requests = result.scalars().all()
    return unresolved_worker_requests

# Marcar un worker_request como resuelto
async def mark_worker_request_as_resolved(
    db: AsyncSession, 
    worker_request_id: int
) -> models.WorkerRequest:
    """
    Marca un WorkerRequest como resuelto (solved=True).
    """
    # Buscar el worker_request por su ID
    worker_request = await db.get(models.WorkerRequest, worker_request_id)
    
    if not worker_request:
        raise HTTPException(status_code=404, detail="WorkerRequest not found")
    
    # Actualizar el estado a resuelto
    worker_request.solved = True
    await db.commit()
    await db.refresh(worker_request)
    
    return worker_request