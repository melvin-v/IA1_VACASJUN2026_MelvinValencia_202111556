import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import Base, engine
from app import models  # noqa: F401
from app.api.routes import (
    health, auth, users, providers, invoices, logs, reports, simulado,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.AUTO_CREATE_TABLES:
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

api = settings.API_V1_PREFIX
for r in (health, auth, users, providers, invoices, logs, reports, simulado):
    app.include_router(r.router, prefix=api if r is not simulado else "")


@app.get("/api")
def api_root():
    return {"message": "SmartInvoice API", "docs": "/docs"}


# Panel web admin (frontend estatico) servido en /app
_static = os.path.join(os.path.dirname(__file__), "static")
app.mount("/app", StaticFiles(directory=_static, html=True), name="frontend")
