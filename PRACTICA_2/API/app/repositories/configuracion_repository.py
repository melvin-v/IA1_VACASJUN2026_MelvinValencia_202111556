from sqlalchemy.orm import Session

from ..models import Configuracion
from .base import BaseRepository


class ConfiguracionRepository(BaseRepository[Configuracion]):
    def __init__(self, db: Session):
        super().__init__(Configuracion, db)

    def get_by_clave(self, clave):
        return (
            self.db.query(Configuracion)
            .filter(Configuracion.clave == clave)
            .first()
        )
