from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.config.database import create_db_and_tables
from src.routers.provas_routes import provas_router
from src.routers.resultados_routes import resultados_router

app = FastAPI()

@app.get('/healthcheck')
def healthcheck():
    return{"status": "ok"}

@asynccontextmanager
async def lifepa(app: FastAPI):
    create_db_and_tables()
    yield
    
app.include_router(provas_router)
app.include_router(resultados_router)