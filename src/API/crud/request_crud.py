from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import models, schemas
from datetime import datetime

# Crear solicitud
async def create_request (db: AsyncSession, request: schemas.RequestCreate):
    db_request = models.Request(**request.dict())
    db.add(db_request)
    await db.commit()
    await db.refresh(db_request)
    return db_request

# Get request by id
async def get_request_by_id(db: AsyncSession, id_request: int):
    result = await db.execute(select(models.Request).filter(models.Request.id == id_request))
    return result.scalars().first()

# Finalizar una solicitud
async def finish_request(db: AsyncSession, id_request: int):
    result = await db.execute(select(models.Request).filter(models.Request.id == id_request))
    request = result.scalars().first()
    request.finish_date = datetime.now()
    await db.commit()
    await db.refresh(request)
    return request

# Cambiar precio de una solicitud
async def change_price_request(db: AsyncSession, id_request: int, price: float):
    result = await db.execute(select(models.Request).filter(models.Request.id == id_request))
    request = result.scalars().first()
    request.price = price
    await db.commit()
    await db.refresh(request)
    return request

# Dar puntuacion a una solicitud
# stand by

# Obtener las solicitudes activas de un solicitante
async def get_active_requests(db : AsyncSession, petitioner_id: int):
    result = await db.execute(select(models.Request).filter(models.Request.id_petitioner == petitioner_id , models.Request.finish_date == None))
    return result

# Ver calificaion de un servicio especifico
async def get_service_evaluation(db: AsyncSession, service_id:int):
    result = await db.execute(select(models.EvaluationPetitioner, models.EvaluationWorker)
                              .join(models.PetitionerService,models.EvaluationPetitiones.id_petitioner_services == models.PetitionerService.id)).join(models.Service, models.PetitionerService.id_services == models.Service.id).filter(models.Service.id == service_id)
    return result