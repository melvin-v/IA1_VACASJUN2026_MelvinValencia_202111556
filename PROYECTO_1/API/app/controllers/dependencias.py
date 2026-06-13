from app.notifiers.telegram_notifier import TelegramNotifier
from app.repositories.historial_repository import HistorialRepository
from app.repositories.prolog_repository import PrologRepository
from app.services.diagnostico_service import DiagnosticoService

_repositorio = PrologRepository()
_notificador = TelegramNotifier()
_historial = HistorialRepository()
_servicio = DiagnosticoService(_repositorio, _notificador, _historial)


def obtener_servicio() -> DiagnosticoService:
    return _servicio