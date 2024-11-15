from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_login(db: AsyncSession, user_login_id: int):
    result = await db.execute(select(models.UserLogin).filter(models.UserLogin.id == user_login_id))
    return result.scalars().first()

# Create user login
async def create_user_login(db: AsyncSession, user_login: schemas.UserLoginCreate, user_id: int):
    db_user_login = models.UserLogin(**user_login.dict(), id_user=user_id)
    db.add(db_user_login)
    await db.commit()
    await db.refresh(db_user_login)
    return db_user_login

async def create_request (db: AsyncSession, request: schemas.RequestCreate, id_petitioner: int):
    db_request = models.Request(**request.dict(), id_petitioner=id_petitioner)
    db.add(db_request)
    await db.commit()
    await db.refresh(db_request)
    return db_request

#Visualizar historial de servicios solicitados
async def visualize_services(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Service).filter(models.Service.finish_date != None, models.Service.id_worker == user_id))
    return result
    
    
#Visualizar perfiles de usuario
async def visualize_user_profile (db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()


#Editar perfil 
async def edit_profile (db: AsyncSession, user_id: int, user: schemas.UserBase):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    user_db = result.scalars().first()
    user_db.name = user.name
    user_db.last_name = user.last_name
    user_db.email = user.email
    user_db.phone = user.phone
    user_db.birthdate = user.birthdate