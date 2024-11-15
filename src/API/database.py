from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


# IMPORTANTE: username y password aun por definir
DATABASE_URL = "postgresql+asyncpg://username:password@localhost/jobbly"

engine = create_async_engine(DATABASE_URL, echo=True)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

