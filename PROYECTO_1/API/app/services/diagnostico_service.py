import uuid
from datetime import datetime

from fastapi import HTTPException

from app.notifiers.telegram_notifier import TelegramNotifier
from app.repositories.historial_repository import HistorialRepository
from app.repositories.prolog_repository import PrologRepository
from app.schemas.diagnostico_schema import (
    DiagnosticoResponse,
    FallaOut,
    SintomaOut,
)
from app.schemas.historial_schema import HistorialItem


class DiagnosticoService:
    def __init__(
        self,
        repositorio: PrologRepository,
        notificador: TelegramNotifier | None = None,
        historial: HistorialRepository | None = None,
    ):
        self._repo = repositorio
        self._notificador = notificador
        self._historial = historial

    def listar_sintomas(self) -> list[SintomaOut]:
        return [SintomaOut(**s) for s in self._repo.listar_sintomas()]

    def diagnosticar(self, sintomas: list[str]) -> DiagnosticoResponse:
        if not sintomas:
            raise HTTPException(
                status_code=400,
                detail="Debe proporcionar al menos un sintoma.",
            )

        unicos: list[str] = []
        for s in sintomas:
            if s not in unicos:
                unicos.append(s)

        validos = {s["id"] for s in self._repo.listar_sintomas()}
        invalidos = [s for s in unicos if s not in validos]
        if invalidos:
            raise HTTPException(
                status_code=400,
                detail=f"Sintoma(s) no reconocido(s): {', '.join(invalidos)}",
            )

        ids_fallas = self._repo.diagnosticar(unicos)
        fallas: list[FallaOut] = []
        for idf in ids_fallas:
            datos = self._repo.obtener_falla(idf)
            if datos:
                fallas.append(FallaOut(**datos))

        if fallas:
            mensaje = f"Se identificaron {len(fallas)} posible(s) falla(s)."
        else:
            mensaje = (
                "No se identificaron fallas con los sintomas proporcionados. "
                "Intente seleccionar sintomas adicionales."
            )

        respuesta = DiagnosticoResponse(
            sintomas_evaluados=unicos,
            fallas=fallas,
            mensaje=mensaje,
        )

        if self._historial is not None:
            registro = {
                "id": uuid.uuid4().hex[:12],
                "fecha": datetime.now().isoformat(timespec="seconds"),
                "sintomas_evaluados": respuesta.sintomas_evaluados,
                "fallas": [f.model_dump() for f in respuesta.fallas],
                "mensaje": respuesta.mensaje,
            }
            self._historial.guardar(registro)

        if self._notificador is not None:
            self._notificador.enviar_diagnostico(respuesta)

        return respuesta

    def listar_historial(self, limite: int | None = None) -> list[HistorialItem]:
        if self._historial is None:
            return []
        return [HistorialItem(**r) for r in self._historial.listar(limite)]
