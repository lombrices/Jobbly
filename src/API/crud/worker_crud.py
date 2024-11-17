from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from .. import models, schemas
from typing import Optional, List

# Crea un trabajador
async def create_worker(db: AsyncSession, worker: models.Worker):
    # Crear un nuevo trabajador
    print("worker:", worker.dict())

    # Verificar si el trabajador ya existe
    db_worker = await db.execute(select(models.Worker).filter(models.Worker.id == worker.id))
    db_worker = db_worker.scalars().first()
    if db_worker:
        raise HTTPException(status_code=404, detail="Worker already exists")
    
    # Verificar si el usuario existe
    db_user = await db.execute(select(models.User).filter(models.User.id == worker.id_user))
    db_user = db_user.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    

    db_worker = models.Worker(**worker.dict())
    db.add(db_worker)
    await db.commit() 
    await db.refresh(db_worker) 

    return db_worker

# Obtiene datos del usuario mediante el id del trabajador
async def get_user_by_worker_id(db: AsyncSession, worker_id: int):
    """
    Obtiene un usuario dado el ID de un trabajador.
    
    :param db: Sesión de la base de datos.
    :param worker_id: ID del trabajador.
    :return: Usuario asociado al trabajador.
    """
    # Realiza la consulta para obtener el usuario asociado al worker_id
    result = await db.execute(
        select(models.User).join(models.Worker).filter(models.Worker.id == worker_id)
    )
    user = result.scalars().first()
    return user