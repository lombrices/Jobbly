from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, database
from ..crud import worker_crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear un trabajador
@router.post("/worker/", response_model=schemas.Worker)
async def create_worker(worker: schemas.WorkerCreate, db: AsyncSession = Depends(get_db)):
    return await worker_crud.create_worker(db, worker)

# # Obtiene datos del usuario mediante el id del trabajador
# @router.get("/worker/{id_worker}", response_model=schemas.User)
# async def get_worker_user(id_worker : int, db : AsyncSession = Depends(get_db)):
# 