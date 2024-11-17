from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from .. import models, schemas, database

# Crear un nuevo registro de petitioner_evaluation
async def create_petitioner_evaluation(
    db: AsyncSession,
    petitioner_evaluation: schemas.EvaluationPetitionerCreate
):
    db_petitioner_evaluation = models.EvaluationPetitioner(**petitioner_evaluation.dict())
    db.add(db_petitioner_evaluation)
    await db.commit()
    await db.refresh(db_petitioner_evaluation)
    return db_petitioner_evaluation

# Obtener un registro de petitioner_evaluation por id
async def get_petitioner_evaluation_by_id(
    db: AsyncSession,
    petitioner_id: int
):
    result = await db.execute(select(models.EvaluationPetitioner).filter(models.EvaluationPetitioner.id == petitioner_id))
    return result.scalars().first()

# Obtener todos los registros de petitioner_evaluation dado un id_service
async def get_petitioners_evaluations_by_id_service(
    db: AsyncSession,
    service_id: int
) -> List[models.EvaluationPetitioner]:
    query = (
        select(models.EvaluationPetitioner)
        .join(models.PetitionerService, models.PetitionerService.id == models.EvaluationPetitioner.id_petitioner_service and models.PetitionerService.id_service == service_id)
    )

    result = await db.execute(query)
    return result.scalars().all()