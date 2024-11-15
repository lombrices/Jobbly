from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import models, schemas

'''
# Create request
async def create_request (db: AsyncSession, request: schemas.RequestCreate, id_petitioner: int):
    db_request = models.Request(**request.dict(), id_petitioner=id_petitioner)
    db.add(db_request)
    await db.commit()
    await db.refresh(db_request)
    return db_request

# Get request by id
async def get_request_by_id(db: AsyncSession, id_request: int):
    result = await db.execute(select(models.Request).filter(models.Request.id == id_request))
    return result.scalars().first()

'''