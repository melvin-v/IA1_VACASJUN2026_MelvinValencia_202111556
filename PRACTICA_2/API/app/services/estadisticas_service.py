from ..repositories.categoria_repository import CategoriaRepository
from ..repositories.consulta_repository import ConsultaRepository
from ..repositories.pregunta_repository import PreguntaRepository


class EstadisticasService:
    def __init__(self, db):
        self.consultas = ConsultaRepository(db)
        self.preguntas = PreguntaRepository(db)
        self.categorias = CategoriaRepository(db)

    def resumen(self):
        total = self.consultas.contar_total()
        respondidas = self.consultas.contar_respondidas()

        return {
            "total_consultas": total,
            "consultas_respondidas": respondidas,
            "consultas_sin_respuesta": total - respondidas,
            "usuarios_unicos": self.consultas.usuarios_unicos(),
            "total_preguntas": len(self.preguntas.get_all()),
            "total_categorias": len(self.categorias.get_all()),
            "consultas_por_categoria": [
                {"etiqueta": nombre, "cantidad": cantidad}
                for nombre, cantidad in self.consultas.consultas_por_categoria()
            ],
            "preguntas_mas_consultadas": [
                {"etiqueta": pregunta, "cantidad": cantidad}
                for pregunta, cantidad in self.consultas.preguntas_mas_consultadas()
            ],
        }
