from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager


# IMPORTANTE: username y password aun por definir
#DATABASE_URL = "postgresql+asyncpg://username:password@localhost/jobbly"
DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost/jobbly"

# Creación del engine para conectar a la base de datos
engine = create_async_engine(DATABASE_URL, echo=True)

# SessionLocal que se utilizará para crear sesiones de la base de datos
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Contexto asíncrono para manejar la sesión de la base de datos
@asynccontextmanager
async def get_db():
    # Se crea una nueva sesión para cada solicitud
    async with sessionLocal() as session:
        yield session
        # Al salir del contexto, se maneja automáticamente el commit o el rollback si es necesario
