from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from .. import models, schemas, database

# Crear un nuevo registro de petitioner_evaluation
async def create_petitioner_evaluation(
    db: AsyncSession,
    petitioner_evaluation: schemas.PetitionerEvaluationCreate
):
    db_petitioner_evaluation = models.PetitionerEvaluation(**petitioner_evaluation.dict())
    db.add(db_petitioner_evaluation)
    await db.commit()
    await db.refresh(db_petitioner_evaluation)
    return db_petitioner_evaluation

# Obtener un registro de petitioner_evaluation por id
async def get_petitioner_evaluation_by_id(
    db: AsyncSession,
    petitioner_id: int
):
    result = await db.execute(select(models.petitionerevaluation).filter(models.PetitionerEvaluation.id == petitioner_id))
    return result.scalars().first()

# Obtener todos los registros de petitioner_evaluation dado un id_services
async def get_petitioners_evaluations_by_id_services(
    db: AsyncSession,
    service_id: int
) -> List[models.petitionerevaluation]:
    query = (
        select(models.petitionerevaluation)
        .join(models.petitionerservices, models.Petitionerservice.id == models.workerevaluation.id_worker_request)
        .join(models.services, models.service.id == models.petitionerRequest.id_request)
        .filter(models.services.id == service_id)
    )
    result = await db.execute(query)
    return result.scalars().all()