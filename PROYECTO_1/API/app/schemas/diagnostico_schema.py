from pydantic import BaseModel, Field


class SintomaOut(BaseModel):
    id: str
    descripcion: str


class DiagnosticoRequest(BaseModel):
    sintomas: list[str] = Field(
        ...,
        description="Lista de IDs de sintomas reportados por el usuario.",
        examples=[["no_enciende", "sin_energia"]],
    )


class FallaOut(BaseModel):
    id: str
    descripcion: str
    recomendacion: str


class DiagnosticoResponse(BaseModel):
    sintomas_evaluados: list[str]
    fallas: list[FallaOut]
    mensaje: str
