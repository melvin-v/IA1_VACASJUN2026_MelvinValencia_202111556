from app.repositories.prolog_repository import PrologRepository
from app.services.diagnostico_service import DiagnosticoService

_repositorio = PrologRepository()
_servicio = DiagnosticoService(_repositorio)


def obtener_servicio() -> DiagnosticoService:
    return _servicio
