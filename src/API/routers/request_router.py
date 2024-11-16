from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, database
from ..crud import request_crud as crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crea un request
@router.post("/request/", response_model=schemas.RequestCreate)
async def create_request(request: schemas.RequestCreate, db: AsyncSession = Depends(get_db)):
    result = await crud.create_request(db=db, request=request) 
    return schemas.Request.from_orm(result)



# Devuleve un request por id
@router.get("/request/{id_request}", response_model=schemas.Request)
async def get_request(request: schemas.Request, db: AsyncSession = Depends(get_db)):
    request = await crud.get_request_by_id(db=db)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return schemas.Request.from_orm(request)

# Finaliza una solicitud
@router.put("/request/{id_request}/finish", response_model=schemas.Request)
async def finish_request(id_request: int, db: AsyncSession = Depends(get_db)):
    response = await crud.finish_request(db=db, id_request=id_request)
    if response is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return schemas.Request.from_orm(response)

# Cambia el precio de una solicitud
@router.put("/request/{id_request}/price", response_model=schemas.Request)
async def change_price_request(id_request: int, price: float, db: AsyncSession = Depends(get_db)):
    response = await crud.change_price_request(db=db, id_request=id_request, price=price)
    if response is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return schemas.Request.from_orm(response)

# Obtener las solicitudes activas de un solicitante
@router.get("/request/{id_petitioner}/active", response_model=List[schemas.Request])
async def get_active_requests(id_petitioner: int, db: AsyncSession = Depends(get_db)):
    result = await crud.get_active_requests(db=db, petitioner_id=id_petitioner)
    return [schemas.Request.from_orm(request) for request in result]

