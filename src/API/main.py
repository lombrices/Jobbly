from fastapi import FastAPI
from .routers import request_router, users_router, services_router, worker_router, petitioner_router, petitioner_service_router, worker_request_router
from . import database
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

# Configuración de los routers (asegúrate de tener los routers correctamente importados)
app.include_router(request_router.router)
app.include_router(users_router.router)
app.include_router(services_router.router)
app.include_router(worker_router.router)
app.include_router(worker_request_router.router)
app.include_router(petitioner_router.router)
app.include_router(petitioner_service_router.router)



# Event handlers para manejar el ciclo de vida de la app
@app.on_event("startup")
async def startup():
    # Aquí puedes agregar cualquier inicialización que necesites al iniciar el servidor
    pass

@app.on_event("shutdown")
async def shutdown():
    # Aquí puedes agregar cualquier tarea de limpieza al apagar el servidor
    pass
