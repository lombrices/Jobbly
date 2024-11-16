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
@router.post("/petitioner", response_model=schemas.Petitioner)
async def create_petitioner(petitioner: schemas.PetitionerCreate, db: AsyncSession = Depends(get_db)):
    return await petitioner_crud.create_petitioner(db, petitioner)