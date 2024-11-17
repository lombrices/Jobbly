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

# Crear un nuevo worker_review
@router.post("/worker_review/", response_model=schemas.WorkerReviewCreate)
async def create_worker_review(
    worker_review: schemas.WorkerReviewCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await worker_review_crud.create_worker_review(db=db, worker_review=worker_review)
    return result

# Obtener un worker_review mediante su id
@router.get("/worker_review/{id}", response_model=schemas.WorkerReview)
async def get_worker_review_by_id(
    worker_review_id: int,
    db: AsyncSession = Depends(get_db)
):
    worker_review = await worker_review_crud.get_worker_review_by_id(db=db, worker_review_id=worker_review_id)
    if worker_review == None:
        raise HTTPException(status_code=404, detail="Worker review not found")
    return schemas.WorkerReview.from_orm(worker_review)

@router.get("/request/{id_request}/review", response_model=List[schemas.WorkerReview])
async def get_worker_review_by_request_id(
    id_request: int,
    db: AsyncSession = Depends(get_db)
):
    worker_reviews = await worker_review_crud.get_workers_reviews_by_id_request(db=db, request_id=id_request)
    if worker_reviews == None:
        raise HTTPException(status_code=404, detail="worker reviews not found")
    return [schemas.WorkerReview.from_orm(worker_review) for worker_review in worker_reviews]
