from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from .. import models, schemas, database

# Crear un nuevo registro de petitioner_review
async def create_petitioner_review(
    db: AsyncSession,
    petitioner_review: schemas.PetitionerReviewCreate
):
    db_petitioner_review = models.PetitionerReview(**petitioner_review.dict())
    db.add(db_petitioner_review)
    await db.commit()
    await db.refresh(db_petitioner_review)
    return db_petitioner_review

# Obtener un registro de petitioner_review por id
async def get_petitioner_review_by_id(
    db: AsyncSession,
    petitioner_review_id: int
):
    result = await db.execute(select(models.PetitionerReview).filter(models.PetitionerReview.id == petitioner_review_id))
    return result.scalars().first()

# Obtener todos los registros de petitioner_review dado un id_worker
async def get_petitioners_reviews_by_id_request(
    db: AsyncSession,
    worker_id: int
) -> List[models.PetitionerReview]:
    query = (
        select(models.PetitionerReview)
        .join(models.WorkerRequest, models.WorkerRequest.id == models.PetitionerReview.id_worker_request and models.WorkerRequest.id_worker == worker_id)
    )
    # query = (
    #     select(models.PetitionerReview)
    #     .join(models.WorkerRequest, models.WorkerRequest.id == models.PetitionerReview.id_worker_request)
    #     .join(models.Request, models.Request.id == models.WorkerRequest.id_request)
    #     .filter(models.Request.id_worker == worker_id)
    # )
    result = await db.execute(query)
    return result.scalars().all()