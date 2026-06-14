from ..models import Consulta
from ..repositories.consulta_repository import ConsultaRepository
from .configuracion_service import ConfiguracionService
from .pregunta_service import PreguntaService

MENSAJE_DEFECTO = (
    "Lo siento, no encontré información sobre tu consulta. "
    "Intenta reformular la pregunta."
)


class ConsultaService:
    def __init__(self, db):
        self.repo = ConsultaRepository(db)
        self.preguntas = PreguntaService(db)
        self.config = ConfiguracionService(db)

    def procesar(self, texto, telegram_user_id, telegram_username):
        pregunta = self.preguntas.buscar_respuesta(texto)

        if pregunta:
            respuesta = pregunta.respuesta
            categoria = pregunta.categoria.nombre if pregunta.categoria else None
            respondida = True
            pregunta_id = pregunta.id
        else:
            respuesta = self.config.valor("mensaje_no_encontrado", MENSAJE_DEFECTO)
            categoria = None
            respondida = False
            pregunta_id = None

        self.repo.create(
            Consulta(
                pregunta_id=pregunta_id,
                telegram_user_id=telegram_user_id,
                telegram_username=telegram_username,
                consulta_texto=texto,
                respuesta_texto=respuesta,
                respondida=respondida,
            )
        )

        return {
            "encontrada": respondida,
            "respuesta": respuesta,
            "categoria": categoria,
        }

    def listar(self):
        return self.repo.listar_recientes()
