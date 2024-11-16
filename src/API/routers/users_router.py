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
    print ("en create_user")
    print ("user: ", user)
    
    user = await users_crud.create_user(db=db, user=user)
    return schemas.User.from_orm(user)


# Obtiene un usuario por id
@router.get("/users/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    print("user_id: ", user_id)
    user = await users_crud.get_user_by_id(db=db, user_id=user_id)
    print("user: ", user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.User.from_orm(user)

# Verifica el login
@router.post("/users/{id}", response_model=schemas.User)
async def get_user_login (id: int, user: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    user = await users_crud.get_user_login(db=db, id=id, user=user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.User.from_orm(user)

# # Obtiene usuarios con filtros
# # Ejemplo de ruta: GET /users/?first_name_starts_with=O&age_greater_than=25
# @router.get("/users/", response_model=List[schemas.User])
# async def read_users(
#     first_name_starts_with: Optional[str] = None,
#     lastname_starts_with: Optional[str] = None,
#     age_greater_than: Optional[int] = None,
#     db: AsyncSession = Depends(get_db)
# ):
#     return await users_crud.get_users(
#         db=db,
#         first_name_starts_with=first_name_starts_with,
#         lastname_starts_with=lastname_starts_with,
#         age_greater_than=age_greater_than
#     )



# # Crea un login de usuario
# @router.post("/user_logins/", response_model=schemas.UserLogin)
# async def create_user_login(user_login: schemas.UserLoginCreate, db: AsyncSession = Depends(get_db)):
#     # Aquí deberías obtener el id del usuario al cual pertenece el login
#     user_id = 1  # Ejemplo, cambia según el flujo
#     return await users_crud.create_user_login(db=db, user_login=user_login, user_id=user_id)
