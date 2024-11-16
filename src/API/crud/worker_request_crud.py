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