from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, database
from ..crud import worker_request_crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para crear un nuevo worker_request
@router.post("/worker_request", response_model=schemas.WorkerRequest)
async def create_worker_request(
    worker_request: schemas.WorkerRequestCreate,
    db: AsyncSession = Depends(get_db)
):
    # Llamamos a la función create_worker_request desde el CRUD
    db_worker_request = await worker_request_crud.create_worker_request(
        db=db, worker_request=worker_request
    )
    return db_worker_request