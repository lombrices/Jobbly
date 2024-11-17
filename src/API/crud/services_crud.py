from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from .. import models, schemas
from typing import Optional, List
from datetime import datetime

# Crea un servicio
async def create_service (db: AsyncSession, service: schemas.ServiceCreate):
    db_service = models.Service(**service.dict())
    db.add(db_service)
    await db.commit()
    await db.refresh(db_service)
    return db_service.scalars().first()

# Obtener servicio por id
async def get_service_by_id(db: AsyncSession, id_service: int):
    result = await db.execute(select(models.Service).filter(models.Service.id == id_service))
    service = result.scalars().first()
    return service.scalars().first()

#Visualizar historial de servicios solicitados
async def visualize_services(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.Service)
        .filter(models.Service.id_worker == user_id)
    )
    return result.scalars().all()

# Finalizar un servicio
async def finish_service(db: AsyncSession, id_service: int):
    result = await db.execute(select(models.Service).filter(models.Service.id == id_service))
    service = result.scalars().first()
    service.finish_date = datetime.now()
    await db.commit()
    await db.refresh(service)
    return service

#Cambiar precio a un servicio
async def change_price_service(db: AsyncSession, service_id: int, price: float):
    result = await db.execute(select(models.Service).filter(models.Service.id == service_id))
    service = result.scalars().first()
    service.price = price
    await db.commit()
    await db.refresh(service)
    return service

#Dar puntuacion a un servicio 
################ESTA RARO ESTE LA VDD :/ ######################
async def rate_service(db: AsyncSession, service_id: int, calification: int):
    result = await db.execute(select(models.PetitionerReview).filter(models.WorkerReview.id_worker_request== service_id))
    service = result.scalars().first()
    service.calification = calification
    await db.commit()
    await db.refresh(service)
    return service

# Obtener los servicios activos de un trabajador
async def get_active_services(db: AsyncSession, worker_id: int):
    result = await db.execute(
        select(models.Service)
        .filter(models.Service.finish_date == None, models.Service.id_worker == worker_id)
    )
    return result.scalars().all()

# Obtener servicios con filtros
# Función para obtener servicios con filtros
async def get_services(
    db: AsyncSession,
    title_contains: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    worker_id: Optional[int] = None
) -> List[models.Service]:
    query = select(models.Service)

    if title_contains:
        query = query.filter(models.Service.title.ilike(f"%{title_contains}%"))

    if min_price:
        query = query.filter(models.Service.price >= min_price)

    if max_price:
        query = query.filter(models.Service.price <= max_price)

    if worker_id:
        query = query.filter(models.Service.id_worker == worker_id)

    result = await db.execute(query.options(joinedload(models.Service.worker)))
    return result.scalars().all()
