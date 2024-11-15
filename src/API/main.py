from fastapi import FastAPI
from .routers import request_router, users_router
from . import database
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

# Configuración de los routers (asegúrate de tener los routers correctamente importados)
app.include_router(request_router.router)
app.include_router(users_router.router)

# Event handlers para manejar el ciclo de vida de la app
@app.on_event("startup")
async def startup():
    # Aquí puedes agregar cualquier inicialización que necesites al iniciar el servidor
    pass

@app.on_event("shutdown")
async def shutdown():
    # Aquí puedes agregar cualquier tarea de limpieza al apagar el servidor
    pass

# # Utilizar la sesión de base de datos en las rutas
# @app.get("/", response_model=None)
# async def get_data(db: AsyncSession = database.get_db()):
#     # Aquí puedes usar la sesión de la base de datos para realizar consultas
#     result = await db.execute("SELECT * FROM users")
#     return {"data": result.fetchall()}
