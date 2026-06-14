from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import Categoria, Consulta, Pregunta
from .base import BaseRepository


class ConsultaRepository(BaseRepository[Consulta]):
    def __init__(self, db: Session):
        super().__init__(Consulta, db)

    def listar_recientes(self, limite=100):
        return (
            self.db.query(Consulta)
            .order_by(Consulta.created_at.desc())
            .limit(limite)
            .all()
        )

    def contar_total(self):
        return self.db.query(func.count(Consulta.id)).scalar()

    def contar_respondidas(self):
        return (
            self.db.query(func.count(Consulta.id))
            .filter(Consulta.respondida.is_(True))
            .scalar()
        )

    def usuarios_unicos(self):
        return self.db.query(
            func.count(func.distinct(Consulta.telegram_user_id))
        ).scalar()

    def consultas_por_categoria(self):
        return (
            self.db.query(Categoria.nombre, func.count(Consulta.id))
            .join(Pregunta, Pregunta.categoria_id == Categoria.id)
            .join(Consulta, Consulta.pregunta_id == Pregunta.id)
            .group_by(Categoria.nombre)
            .order_by(func.count(Consulta.id).desc())
            .all()
        )

    def preguntas_mas_consultadas(self, limite=5):
        return (
            self.db.query(Pregunta.pregunta, func.count(Consulta.id))
            .join(Consulta, Consulta.pregunta_id == Pregunta.id)
            .group_by(Pregunta.pregunta)
            .order_by(func.count(Consulta.id).desc())
            .limit(limite)
            .all()
        )
