from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from .. import models, schemas
from typing import Optional, List

## Funcion get_users que permite filtros
async def get_users(
    db: AsyncSession,
    first_name_starts_with: Optional[str] = None,
    lastname_starts_with: Optional[str] = None,
    age_greater_than: Optional[int] = None
) -> List[models.User]:
    query = select(models.User)
    
    if first_name_starts_with:
        query = query.filter(models.User.first_name.like(f"{first_name_starts_with}%"))
    
    if lastname_starts_with:
        query = query.filter(models.User.lastname.like(f"{lastname_starts_with}%"))
    
    if age_greater_than:
        query = query.filter(models.User.age > age_greater_than)
    
    result = await db.execute(query)
    return result.scalars().all()

# Obtiene un usuario por id
async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    user = result.scalars().first()
    return user

#Crear usuario
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

 #Visualizar perfiles de usuario
async def visualize_user_profile (db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

# Editar perfil 
async def edit_profile (db: AsyncSession, user_id: int, user: schemas.UserBase):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    user_db = result.scalars().first()
    user_db.lastname = user.lastname
    user_db.phone_number = user.phone_number

# Cambiar contraseña
async def change_password (db: AsyncSession, user_id: int, user: schemas.UserLogin):
    result = await db.execute(select(models.UserLogin).filter(models.UserLogin.id_user == user_id))
    user_db = result.scalars().first()
    user_db.pass_hash = user.pass_hash

# Create user login
async def create_user_login(db: AsyncSession, user_login: schemas.UserLoginCreate):
    # Verificamos que el mail no exista
    db_user_login = await db.execute(select(models.UserLogin).filter(models.UserLogin.mail == user_login.mail))
    db_user_login = db_user_login.scalars().first()
    if db_user_login:
      raise HTTPException(status_code=404, detail="The mail already exists")

    db_user_login = models.UserLogin(**user_login.dict())
    db.add(db_user_login)
    await db.commit()
    await db.refresh(db_user_login)
    return db_user_login

# Verificar login
async def get_user_login(db: AsyncSession, mail: str):
    result = await db.execute(select(models.UserLogin).filter(models.UserLogin.mail == mail))
    return result.scalars().first()