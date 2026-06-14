from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..schemas import ConfiguracionOut, ConfiguracionUpdate
from ..services.configuracion_service import ConfiguracionService

router = APIRouter(
    prefix="/configuracion",
    tags=["configuracion"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=List[ConfiguracionOut])
def listar(db: Session = Depends(get_db)):
    return ConfiguracionService(db).listar()


@router.get("/{clave}", response_model=ConfiguracionOut)
def obtener(clave: str, db: Session = Depends(get_db)):
    return ConfiguracionService(db).obtener(clave)


@router.put("/{clave}", response_model=ConfiguracionOut)
def actualizar(
    clave: str, data: ConfiguracionUpdate, db: Session = Depends(get_db)
):
    return ConfiguracionService(db).actualizar(clave, data.valor)
