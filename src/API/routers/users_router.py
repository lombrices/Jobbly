from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, database
from ..crud import users_crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crea un usuario
@router.post("/users/", response_model=schemas.UserCreate)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    user = await users_crud.create_user(db=db, user=user)
    return schemas.User.from_orm(user)


# Obtiene un usuario por id
@router.get("/users/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await users_crud.get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.User.from_orm(user)


"""
Obtiene un usuario con filtros opcionales.
    - **first_name_starts_with**: Filtra usuarios cuyo nombre comience con este valor.
    - **lastname_starts_with**: Filtra usuarios cuyo apellido comience con este valor.
    - **age_greater_than**: Filtra usuarios con edad mayor que este valor.
"""

@router.get("/users", response_model=List[schemas.User])
async def get_users_with_filters(
    first_name_starts_with: Optional[str] = None,
    lastname_starts_with: Optional[str] = None,
    age_greater_than: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    # Llamar a la función en el CRUD
    users = await users_crud.get_users(
        db=db,
        first_name_starts_with=first_name_starts_with,
        lastname_starts_with=lastname_starts_with,
        age_greater_than=age_greater_than
    )
    
    # Verificar si se encontraron usuarios
    if not users:
        raise HTTPException(status_code=404, detail="No users found with the provided filters")
    
    # Retornar los usuarios mapeados a los esquemas
    return [schemas.User.from_orm(user) for user in users]

# Verifica el login mediante user_login
@router.get("/user_login/{mail}", response_model=schemas.UserLogin)
async def get_user_login (mail: str, db: AsyncSession = Depends(get_db)):
    user_login = await users_crud.get_user_login(db=db, mail=mail)
    if user_login is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserLogin.from_orm(user_login)

# Crea un user_login
@router.post("/user_login/", response_model=schemas.UserLoginCreate)
async def post_user_login (user_login:schemas.UserLoginCreate, db:AsyncSession = Depends(get_db)):
    user_login = await users_crud.create_user_login(db=db, user_login=user_login)
    return schemas.UserLogin.from_orm(user_login)