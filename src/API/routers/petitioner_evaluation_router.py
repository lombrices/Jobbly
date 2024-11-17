from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, database
from ..crud import petitioner_evaluation_crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crea un petitioner_evaluation
@router.post("/petitioner_evaluation/", response_model=schemas.EvaluationPetitionerCreate)
async def create_petitioner_evaluation(
    petitioner_evaluation: schemas.petitionerEvaluationCreate, 
    db: AsyncSession = Depends(get_db)
):
    result = await petitioner_evaluation_crud.create_petitioner_evaluation(db=db, petitioner_evaluation=petitioner_evaluation)
    return schemas.EvaluationPetitioner(result)

# Obtiene un petitioner_evaluation dado su id
@router.get("/petitioner_evaluation/{id}", response_model=schemas.PetitionerEvaluation)
async def get_petitioner_evaluation_by_id(
    id_petitioner_evaluation: int,
    db: AsyncSession = Depends(get_db)
):
    petitioner_evaluation = await petitioner_evaluation_crud.get_petitioner_review_by_id(db=db, petitioner_id=id_petitioner_evaluation)
    if petitioner_evaluation == None:
        raise HTTPException(status_code=404, detail="Petitioner evaluation not found")
    return schemas.EvaluationPetitioner.form_orm(petitioner_evaluation)

# Obtiene todos los reviews de un servicio dado su id
@router.get("/service/{id_service}/reviews/", response_model=List[schemas.EvaluationPetitioner])
async def get_service_reviews(
    id_service: int,
    db: AsyncSession = Depends(get_db)
):
    petitioner_evaluations = await petitioner_evaluation_crud.get_petitioners_evaluations_by_id_services(db=db, id_service=id_service)
    if petitioner_evaluations == None:
        raise HTTPException(status_code=404, detail="Petitioners reviews not found")
    return [schemas.EvaluationPetitioner.from_orm(petitioner_evaluation) for petitioner_evaluation in petitioner_evaluations]