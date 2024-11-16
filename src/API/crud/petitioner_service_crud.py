from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import models, schemas, database
from datetime import datetime

# Crear un nuevo registro de petitioner_service
async def create_petitioner_service(
    db: AsyncSession,
    petitioner_service: schemas.PetitionerServiceCreate
):
    # Crear una instancia del modelo PetitionerService
    db_petitioner_service = models.PetitionerService(
        id_services=petitioner_service.id_services,
        id_petitioner=petitioner_service.id_petitioner,
        petition_date=petitioner_service.petition_date,
        solved=petitioner_service.solved
    )

    # Añadir la instancia a la sesión de base de datos
    db.add(db_petitioner_service)
    # Confirmar los cambios en la base de datos
    await db.commit()
    # Refrescar el objeto para obtener el ID generado
    await db.refresh(db_petitioner_service)

    return db_petitioner_service