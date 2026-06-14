from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..schemas import CategoriaCreate, CategoriaOut, CategoriaUpdate
from ..services.categoria_service import CategoriaService

router = APIRouter(
    prefix="/categorias",
    tags=["categorias"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=List[CategoriaOut])
def listar(db: Session = Depends(get_db)):
    return CategoriaService(db).listar()


@router.get("/{categoria_id}", response_model=CategoriaOut)
def obtener(categoria_id: int, db: Session = Depends(get_db)):
    return CategoriaService(db).obtener(categoria_id)


@router.post("", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
def crear(data: CategoriaCreate, db: Session = Depends(get_db)):
    return CategoriaService(db).crear(data)


@router.put("/{categoria_id}", response_model=CategoriaOut)
def actualizar(
    categoria_id: int, data: CategoriaUpdate, db: Session = Depends(get_db)
):
    return CategoriaService(db).actualizar(categoria_id, data)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(categoria_id: int, db: Session = Depends(get_db)):
    CategoriaService(db).eliminar(categoria_id)
