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
    petitioner_evaluation: schemas.EvaluationPetitionerCreate, 
    db: AsyncSession = Depends(get_db)
):
    result = await petitioner_evaluation_crud.create_petitioner_evaluation(db=db, petitioner_evaluation=petitioner_evaluation)
    return schemas.EvaluationPetitioner.from_orm(result)

# Obtiene un petitioner_evaluation dado su id
@router.get("/petitioner_evaluation/{id}", response_model=schemas.EvaluationPetitioner)
async def get_petitioner_evaluation_by_id(
    id_petitioner_evaluation: int,
    db: AsyncSession = Depends(get_db)
):
    petitioner_evaluation = await petitioner_evaluation_crud.get_petitioner_evaluation_by_id(db=db, petitioner_id=id_petitioner_evaluation)
    if petitioner_evaluation == None:
        raise HTTPException(status_code=404, detail="Petitioner evaluation not found")
    return schemas.EvaluationPetitioner.from_orm(petitioner_evaluation)

# Obtiene todos los evaluations de un servicio dado su id
@router.get("/service/{id_service}/evaluations/", response_model=List[schemas.EvaluationPetitioner])
async def get_service_evaluations(
    id_service: int,
    db: AsyncSession = Depends(get_db)
):
    petitioner_evaluations = await petitioner_evaluation_crud.get_petitioners_evaluations_by_id_service(db=db, service_id=id_service)
    if petitioner_evaluations == None:
        raise HTTPException(status_code=404, detail="Petitioners evaluations not found")
    return [schemas.EvaluationPetitioner.from_orm(petitioner_evaluation) for petitioner_evaluation in petitioner_evaluations]