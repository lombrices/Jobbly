from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, database
from ..crud import worker_evaluation_crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crea un worker_evaluation
@router.post("/worker_evaluation/", response_model=schemas.EvaluationWorkerCreate)
async def create_worker_evaluation(
    worker_evaluation: schemas.EvaluationWorkerCreate, 
    db: AsyncSession = Depends(get_db)
):
    result = await worker_evaluation_crud.create_worker_evaluation(db=db, worker_evaluation=worker_evaluation)
    return schemas.workerevaluation.from_orm(result)


# Obtiene un worker_evaluation dado su id
@router.get("/worker_evaluation/{id}", response_model=schemas.EvaluationWorker)
async def get_worker_evaluation_by_id(
    id_worker_evaluation: int,
    db: AsyncSession = Depends(get_db)
):
    worker_evaluation = await worker_evaluation_crud.get_worker_evaluatin_by_id(db=db, worker_evaluation_id=id_worker_evaluation)
    if worker_evaluation == None:
        raise HTTPException(status_code=404, detail="worker evaluation not found")
    return schemas.EvaluationWorker.from_orm(worker_evaluation)


# Obtiene todas las evaluaciones de un trabajador dado un id de trabajador
@router.get("/petitioner/{id_petitioner}/evaluation", response_model=List[schemas.EvaluationWorker])
async def get_worker_evaluations_by_id(
    id_petitoner: int,
    db: AsyncSession = Depends(get_db)
):
    worker_evaluations = await worker_evaluation_crud.get_workers_evaluations_by_id_petitioner(db=db, id_petitioner=id_petitoner)
    if worker_evaluations == None:
        raise HTTPException(status_code=404, detail="Petitoners evaluations are not found")
    return [schemas.EvaluationWorker.from_orm(worker_evaluation) for worker_evaluation in worker_evaluations]