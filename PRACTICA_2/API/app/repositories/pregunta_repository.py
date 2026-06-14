from sqlalchemy.orm import Session

from ..models import Pregunta
from .base import BaseRepository


class PreguntaRepository(BaseRepository[Pregunta]):
    def __init__(self, db: Session):
        super().__init__(Pregunta, db)

    def get_by_categoria(self, categoria_id):
        return (
            self.db.query(Pregunta)
            .filter(Pregunta.categoria_id == categoria_id)
            .all()
        )
