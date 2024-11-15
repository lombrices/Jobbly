from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, database
from ..crud import request_crud as crud

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # Crea un request
# @router.post("/request/", response_model=schemas.RequestCreate)
# async def create_request(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
#     return await crud.create_request(db=db, user=user)

# # Devuleve un request por id
# @router.get("/request/{id_request}", response_model=schemas.Request)
# async def get_request(request: schemas.Request, db: AsyncSession = Depends(get_db)):
#     response = await crud.get_request_by_id(db=db, id_request=id_request)
#     if response is None:
#         raise HTTPException(status_code=404, detail="Request not found")
#     return response