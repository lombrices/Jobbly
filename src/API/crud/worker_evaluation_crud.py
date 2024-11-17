from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from .. import models, schemas, database

# Crear un nuevo registro de worker_evaluation
async def create_worker_evaluation(
    db: AsyncSession,
    worker_evaluation: schemas.WorkerEvaluationCreate
):
    db_worker_evaluation = models.WorkerEvaluation(**worker_evaluation.dict())
    db.add(db_worker_evaluation)
    await db.commit()
    await db.refresh(db_worker_evaluation)
    return db_worker_evaluation

# Obtener un registro de worker_evaluation por id
async def get_worker_evaluation_by_id(
    db: AsyncSession,
    worker_id: int
):
    result = await db.execute(select(models.workerevaluation).filter(models.WorkerEvaluation.id == worker_id))
    return result.scalars().first()

# Obtener todos los registros de worker_evaluation dado un id_services
async def get_workers_evaluations_by_id_services(
    db: AsyncSession,
    service_id: int
) -> List[models.workerevaluation]:
    query = (
        select(models.workerevaluation)
        .join(models.workerservices, models.Workerservice.id == models.workerevaluation.id_worker_request)
        .join(models.services, models.service.id == models.workerservice.id_request)
        .filter(models.services.id == service_id)
    )
    result = await db.execute(query)
    return result.scalars().all()