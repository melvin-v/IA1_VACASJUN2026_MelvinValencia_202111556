from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..schemas import ConsultaOut
from ..services.consulta_service import ConsultaService

router = APIRouter(
    prefix="/consultas",
    tags=["consultas"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=List[ConsultaOut])
def listar(db: Session = Depends(get_db)):
    return ConsultaService(db).listar()
