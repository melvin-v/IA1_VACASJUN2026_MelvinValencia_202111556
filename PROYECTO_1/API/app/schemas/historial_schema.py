from pydantic import BaseModel

from app.schemas.diagnostico_schema import FallaOut


class HistorialItem(BaseModel):
    id: str
    fecha: str 
    sintomas_evaluados: list[str]
    fallas: list[FallaOut]
    mensaje: str
