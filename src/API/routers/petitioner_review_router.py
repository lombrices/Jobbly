from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, database
from ..crud import petitioner_review_crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crea un petitioner_review
@router.post("/petitioner_review/", response_model=schemas.PetitionerReviewCreate)
async def create_petitioner_review(
    petitioner_review: schemas.PetitionerReviewCreate, 
    db: AsyncSession = Depends(get_db)
):
    result = await petitioner_review_crud.create_petitioner_review(db=db, petitioner_review=petitioner_review)
    return schemas.PetitionerReview.from_orm(result)

# Obtiene un petitioner_review dado su id
@router.get("/petitioner_review/{id}", response_model=schemas.PetitionerReview)
async def get_petitioner_review_by_id(
    id_petitioner_review: int,
    db: AsyncSession = Depends(get_db)
):
    petitioner_review = await petitioner_review_crud.get_petitioner_review_by_id(db=db, petitioner_review_id=id_petitioner_review)
    if petitioner_review == None:
        raise HTTPException(status_code=404, detail="Petitioner review not found")
    return schemas.PetitionerReview.from_orm(petitioner_review)

# Obtiene todas las evaluaciones de un trabajador dado un id de trabajador
@router.get("/worker/{id_worker}/evaluation", response_model=List[schemas.PetitionerReview])
async def get_worker_reviews_by_id(
    id_worker: int,
    db: AsyncSession = Depends(get_db)
):
    petitioner_reviews = await petitioner_review_crud.get_petitioners_reviews_by_id_request(db=db, worker_id=id_worker)
    if petitioner_reviews == None:
        raise HTTPException(status_code=404, detail="Petitoners reviews are not found")
    return [schemas.PetitionerReview.from_orm(petitioner_review) for petitioner_review in petitioner_reviews]