from sqlalchemy.orm import Session

from ..models import UsuarioAdmin
from .base import BaseRepository


class UsuarioRepository(BaseRepository[UsuarioAdmin]):
    def __init__(self, db: Session):
        super().__init__(UsuarioAdmin, db)

    def get_by_username(self, username):
        return (
            self.db.query(UsuarioAdmin)
            .filter(UsuarioAdmin.username == username)
            .first()
        )
