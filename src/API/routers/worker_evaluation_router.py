from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, database
from ..crud import worker_review_crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crea un worker_review
@router.post("/worker_review/", response_model=schemas.WorkerReviewCreate)
async def create_worker_review(
    worker_review: schemas.petitionerReviewCreate, 
    db: AsyncSession = Depends(get_db)
):
    result = await worker_review_crud.create_petitioner_review(db=db, petitioner_review=petitioner_review)
    return schemas.workerReview.form_orm(result)

# Obtiene un worker_review dado su id
@router.get("/worker_review/{id}", response_model=schemas.WorkerReview)
async def get_worker_review_by_id(
    id_worker_review: int,
    db: AsyncSession = Depends(get_db)
):
    worker_review = await petitioner_review_crud.get_petitioner_review_by_id(db=db, petitioner_id=id_petitioner_review)
    if worker_review == None:
        raise HTTPException(status_code=404, detail="worker review not found")
    return schemas.workerReview.form_orm(petitioner_review)

# Obtiene todas las evaluaciones de un trabajador dado un id de trabajador
@router.get("/petitioner/{id_petitioner}/evaluation", response_model=List[schemas.workerReview])
async def get_worker_reviews_by_id(
    id_worker: int,
    db: AsyncSession = Depends(get_db)
):
    worker_reviews = await petitioner_review_crud.get_petitioners_reviews_by_id_worker(db=db, id_worker=id_worker)
    if worker_reviews == None:
        raise HTTPException(status_code=404, detail="Petitoners reviews are not found")
    return [schemas.workerReview.form_orm(petitioner_review) for petitioner_review in petitioner_reviews]