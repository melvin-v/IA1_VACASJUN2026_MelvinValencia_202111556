from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class CategoriaOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PreguntaCreate(BaseModel):
    categoria_id: int
    pregunta: str
    respuesta: str
    palabras_clave: Optional[str] = None


class PreguntaUpdate(BaseModel):
    categoria_id: Optional[int] = None
    pregunta: Optional[str] = None
    respuesta: Optional[str] = None
    palabras_clave: Optional[str] = None


class PreguntaOut(BaseModel):
    id: int
    categoria_id: int
    pregunta: str
    respuesta: str
    palabras_clave: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    categoria: Optional[CategoriaOut] = None

    model_config = {"from_attributes": True}


class ConfiguracionOut(BaseModel):
    clave: str
    valor: Optional[str] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ConfiguracionUpdate(BaseModel):
    valor: str = ""


class ConsultaBotRequest(BaseModel):
    texto: str
    telegram_user_id: Optional[int] = None
    telegram_username: Optional[str] = None


class ConsultaBotResponse(BaseModel):
    encontrada: bool
    respuesta: str
    categoria: Optional[str] = None


class ConsultaOut(BaseModel):
    id: int
    pregunta_id: Optional[int] = None
    telegram_user_id: Optional[int] = None
    telegram_username: Optional[str] = None
    consulta_texto: str
    respuesta_texto: Optional[str] = None
    respondida: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ConteoItem(BaseModel):
    etiqueta: str
    cantidad: int


class EstadisticasOut(BaseModel):
    total_consultas: int
    consultas_respondidas: int
    consultas_sin_respuesta: int
    usuarios_unicos: int
    total_preguntas: int
    total_categorias: int
    consultas_por_categoria: List[ConteoItem]
    preguntas_mas_consultadas: List[ConteoItem]
