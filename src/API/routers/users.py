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

async def create_user_login(db: AsyncSession, user_login: schemas.UserLoginCreate, user_id: int):
    db_user_login = models.UserLogin(**user_login.dict(), id_user=user_id)
    db.add(db_user_login)
    await db.commit()
    await db.refresh(db_user_login)
    return db_user_login