from fastapi import FastAPI
from .routers import jobs
from . import models, database

async def run_db(app:FastAPI):
    # Iniciamos la base de datos
    async with database.engine.begin() as conn:
        await conn.runt_sync(models.Base.metadata.create_all)

app = FastAPI(lifespan=run_db)

app.include_router(jobs.router, prefix="/api", tags=["jobs"])