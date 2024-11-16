from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import models, schemas
from datetime import datetime

# Create service
async def create_service (db: AsyncSession, service: schemas.ServiceCreate, id_worker: int):
    db_service = models.Service(**service.dict(), id_worker=id_worker)
    db.add(db_service)
    await db.commit()
    await db.refresh(db_service)
    return db_service

# Obtener servicio por id
async def get_service_by_id(db: AsyncSession, id_service: int):
    result = await db.execute(select(models.Service).filter(models.Service.id == id_service))
    service = result.scalars().first()
    return service

#Visualizar historial de servicios solicitados
async def visualize_services(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Service).filter(models.Service.finish_date != None, models.Service.id_worker == user_id))
    return result

#Cambiar estado del servicio o eliminarlo
async def change_status_service(db: AsyncSession, service_id: int):
    result = await db.execute(select(models.Service).filter(models.Service.id == service_id))
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
async def get_active_services(db : AsyncSession, worker_id: int):
    result = await db.execute(select(models.Service).filter(models.Service.id_worker == worker_id , models.Service.finish_date == None))
    return result

# Ver reseñas asociadas a