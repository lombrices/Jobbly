from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, database
from ..crud import services_crud as crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crea un servicio
@router.post("/services/", response_model=schemas.ServiceCreate)
async def create_service(service: schemas.ServiceCreate, db: AsyncSession = Depends(get_db)):
    result = await crud.create_service(db=db, service=service)
    return schemas.Service.from_orm(result)

# Obtiene un servicio por id
@router.get("/services/{id_service}", response_model=schemas.Service)
async def get_service_by_id(id_service: int, db: AsyncSession = Depends(get_db)):
    result = await crud.get_service_by_id(db=db, id_service=id_service)
    if result is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return schemas.Service.from_orm(result)

# Visualiza historial de servicios solicitados
@router.get("/services/{id_worker}/history", response_model=List[schemas.Service])
async def visualize_services(id_worker: int, db: AsyncSession = Depends(get_db)):
    result = await crud.visualize_services(db=db, user_id=id_worker)
    return [schemas.Service.from_orm(service) for service in result]

# Finaliza un servicio
@router.put("/services/{id_service}/finish", response_model=schemas.Service)
async def finish_service(id_service: int, db: AsyncSession = Depends(get_db)):
    result = await crud.finish_service(db=db, id_service=id_service)
    if result is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return schemas.Service.from_orm(result)

# Cambia el precio de un servicio
@router.put("/services/{id_service}/price", response_model=schemas.Service)
async def change_price_service(id_service: int, price: float, db: AsyncSession = Depends(get_db)):
    result = await crud.change_price_service(db=db, service_id=id_service, price=price)
    if result is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return schemas.Service.from_orm(result)

# Obtiene los servicios activos de un trabajador
@router.get("/services/{id_worker}/active", response_model=List[schemas.Service])
async def get_active_services(id_worker: int, db: AsyncSession = Depends(get_db)):
    result = await crud.get_active_services(db=db, worker_id=id_worker)
    return [schemas.Service.from_orm(service) for service in result]

# Obtener servicios con filtros
@router.get("/services", response_model=List[schemas.Service])
async def get_services(
    title: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    worker_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    services = await crud.get_services(
        db=db, 
        title_contains=title, 
        min_price=min_price, 
        max_price=max_price, 
        worker_id=worker_id
    )
    if not services:
        raise HTTPException(status_code=404, detail="No services found")
    return [schemas.Service.from_orm(service) for service in services]