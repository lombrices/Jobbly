from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from .. import models, schemas
from typing import Optional, List


# Crea un solicitante
async def create_petitioner(db: AsyncSession, petitioner: models.Petitioner):
    # Crear un nuevo solicitante
    print("petitioner:", petitioner.dict())

    # Verificar si el solicitante ya existe
    db_petitioner = await db.execute(select(models.Petitioner).filter(models.Petitioner.id_user == petitioner.id_user))
    db_petitioner = db_petitioner.scalars().first()
    if db_petitioner:
        raise HTTPException(status_code=400, detail="Petitioner already exists")
    
    # Verificar si el usuario existe
    db_user = await db.execute(select(models.User).filter(models.User.id == petitioner.id_user))
    db_user = db_user.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    

    db_petitioner = models.Petitioner(**petitioner.dict())
    db.add(db_petitioner)
    await db.commit() 
    await db.refresh(db_petitioner) 

    return db_petitioner
