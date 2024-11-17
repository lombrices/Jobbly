from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, database
from ..crud import petitioner_crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear un solicitante
@router.post("/petitioner/", response_model=schemas.Petitioner)
async def create_petitioner(petitioner: schemas.PetitionerCreate, db: AsyncSession = Depends(get_db)):
    return await petitioner_crud.create_petitioner(db, petitioner)

# Obtiene datos del usuario mediante el id del trabajador
@router.get("/petitioner/{petitioner_id}")
async def get_petitioner_user(petitioner_id: int, db: AsyncSession = Depends(get_db)):
    user = await petitioner_crud.get_user_by_petitioner_id(db=db, petitioner_id=petitioner_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.EvaluationPetitioner.form_orm(user)
