from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from .. import models, schemas, database

# Crear un nuevo registro de worker_evaluation
async def create_worker_evaluation(
    db: AsyncSession,
    worker_evaluation: schemas.EvaluationWorkerCreate
):
    db_worker_evaluation = models.EvaluationWorker(**worker_evaluation.dict())
    db.add(db_worker_evaluation)
    await db.commit()
    await db.refresh(db_worker_evaluation)
    return db_worker_evaluation

# Obtener un registro de worker_evaluation por id
async def get_worker_evaluation_by_id(
    db: AsyncSession,
    worker_evaluation_id: int
):
    result = await db.execute(select(models.EvaluationWorker).filter(models.EvaluationWorker.id == worker_evaluation_id))
    return result.scalars().first()

# Obtener todos los registros de worker_evaluation dado un id_petitioner
async def get_workers_evaluations_by_id_petitioner(
    db: AsyncSession,
    id_petitioner: int
) -> List[models.EvaluationWorker]:
    query = (
        select(models.EvaluationWorker)
        .join(models.PetitionerService, models.PetitionerService.id == models.EvaluationWorker.id_petitioner_service)
        .filter(models.PetitionerService.id_petitioner == id_petitioner)
    )

    result = await db.execute(query)
    return result.scalars().all()