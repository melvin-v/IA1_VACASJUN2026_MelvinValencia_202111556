from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import (
    auth,
    bot,
    categorias,
    configuracion,
    consultas,
    estadisticas,
    preguntas,
)
from .seed import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed()
    yield


app = FastAPI(title="SmartBot API", version="1.0.0", lifespan=lifespan)

if settings.cors_origins == "*":
    origins = ["*"]
else:
    origins = [o.strip() for o in settings.cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categorias.router)
app.include_router(preguntas.router)
app.include_router(configuracion.router)
app.include_router(consultas.router)
app.include_router(estadisticas.router)
app.include_router(bot.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "SmartBot API"}
