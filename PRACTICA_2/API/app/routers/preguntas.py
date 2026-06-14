from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..schemas import PreguntaCreate, PreguntaOut, PreguntaUpdate
from ..services.pregunta_service import PreguntaService

router = APIRouter(
    prefix="/preguntas",
    tags=["preguntas"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=List[PreguntaOut])
def listar(db: Session = Depends(get_db)):
    return PreguntaService(db).listar()


@router.get("/{pregunta_id}", response_model=PreguntaOut)
def obtener(pregunta_id: int, db: Session = Depends(get_db)):
    return PreguntaService(db).obtener(pregunta_id)


@router.post("", response_model=PreguntaOut, status_code=status.HTTP_201_CREATED)
def crear(data: PreguntaCreate, db: Session = Depends(get_db)):
    return PreguntaService(db).crear(data)


@router.put("/{pregunta_id}", response_model=PreguntaOut)
def actualizar(
    pregunta_id: int, data: PreguntaUpdate, db: Session = Depends(get_db)
):
    return PreguntaService(db).actualizar(pregunta_id, data)


@router.delete("/{pregunta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(pregunta_id: int, db: Session = Depends(get_db)):
    PreguntaService(db).eliminar(pregunta_id)
