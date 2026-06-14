from sqlalchemy.orm import Session

from ..models import Categoria
from .base import BaseRepository


class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, db: Session):
        super().__init__(Categoria, db)

    def get_by_nombre(self, nombre):
        return (
            self.db.query(Categoria).filter(Categoria.nombre == nombre).first()
        )
