from app.notifiers.telegram_notifier import TelegramNotifier
from app.repositories.prolog_repository import PrologRepository
from app.services.diagnostico_service import DiagnosticoService

_repositorio = PrologRepository()
_notificador = TelegramNotifier()
_servicio = DiagnosticoService(_repositorio, _notificador)


def obtener_servicio() -> DiagnosticoService:
    return _servicio