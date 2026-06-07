from pydantic import BaseModel, field_validator
from typing import List


class RutaResponse(BaseModel):
    camino: List[str]
    distancia_km: int
    num_paradas: int


class RutaMasCorta(BaseModel):
    origen: str
    destino: str
    ruta: RutaResponse
    mensaje: str


class TodasLasRutas(BaseModel):
    origen: str
    destino: str
    total_rutas: int
    rutas: List[RutaResponse]


class CiudadesResponse(BaseModel):
    ciudades: List[str]
    total: int


class MensajeResponse(BaseModel):
    exito: bool
    mensaje: str


class NuevaCiudad(BaseModel):
    nombre: str

    @field_validator("nombre")
    @classmethod
    def nombre_valido(cls, v: str) -> str:
        nombre = v.strip().lower().replace(" ", "_")
        if not nombre:
            raise ValueError("El nombre no puede estar vacio")
        if not nombre.replace("_", "").isalpha():
            raise ValueError("El nombre solo puede contener letras y espacios")
        return nombre


class NuevaConexion(BaseModel):
    ciudad_a: str
    ciudad_b: str
    distancia_km: int

    @field_validator("distancia_km")
    @classmethod
    def distancia_positiva(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("La distancia debe ser mayor a 0")
        return v