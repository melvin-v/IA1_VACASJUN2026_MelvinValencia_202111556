from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import verify_bot_key
from ..schemas import ConsultaBotRequest, ConsultaBotResponse
from ..services.consulta_service import ConsultaService

router = APIRouter(
    prefix="/bot",
    tags=["bot"],
    dependencies=[Depends(verify_bot_key)],
)


@router.post("/consultar", response_model=ConsultaBotResponse)
def consultar(data: ConsultaBotRequest, db: Session = Depends(get_db)):
    return ConsultaService(db).procesar(
        data.texto, data.telegram_user_id, data.telegram_username
    )
