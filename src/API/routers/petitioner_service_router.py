from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, database
from ..crud import petitioner_service_crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para crear un nuevo petitioner_service
@router.post("/petitioner_service", response_model=schemas.PetitionerService)
async def create_petitioner_service(
    petitioner_service: schemas.PetitionerServiceCreate,
    db: AsyncSession = Depends(get_db)
):
    # Llamamos a la función create_petitioner_service desde el CRUD
    db_petitioner_service = await petitioner_service_crud.create_petitioner_service(
        db=db, petitioner_service=petitioner_service
    )
    return db_petitioner_service