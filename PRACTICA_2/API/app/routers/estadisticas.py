from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..schemas import EstadisticasOut
from ..services.estadisticas_service import EstadisticasService

router = APIRouter(
    prefix="/estadisticas",
    tags=["estadisticas"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=EstadisticasOut)
def resumen(db: Session = Depends(get_db)):
    return EstadisticasService(db).resumen()
