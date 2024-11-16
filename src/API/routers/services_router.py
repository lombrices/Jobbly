from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, database
from ..crud import services_crud as crud

router = APIRouter()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()