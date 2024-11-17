from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from .. import models, schemas, database

# Crear un nuevo registro de worker_review
async def create_worker_review(
    db: AsyncSession,
    worker_review: schemas.WorkerReviewCreate
):
    db_worker_review = models.WorkerReview(**worker_review.dict())
    db.add(db_worker_review)
    await db.commit()
    await db.refresh(db_worker_review)
    return db_worker_review

# Obtener un registro de worker_review por id
async def get_worker_review_by_id(
    db: AsyncSession,
    worker_review_id: int
):
    result = await db.execute(select(models.WorkerReview).filter(models.WorkerReview.id == worker_review_id))
    return result.scalars().first()

# Obtener todos los registros de worker_review dado un id_request
async def get_workers_reviews_by_id_request(
    db: AsyncSession,
    request_id: int
) -> List[models.WorkerReview]:
    query = (
        select(models.WorkerReview)
        .join(models.WorkerRequest, models.WorkerRequest.id == models.WorkerReview.id_worker_request)
        .join(models.Request, models.Request.id == models.WorkerRequest.id_request)
        .filter(models.Request.id == request_id)
    )
    result = await db.execute(query)
    return result.scalars().all()