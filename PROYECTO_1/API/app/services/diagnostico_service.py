from fastapi import HTTPException

from app.repositories.prolog_repository import PrologRepository
from app.schemas.diagnostico_schema import (
    DiagnosticoResponse,
    FallaOut,
    SintomaOut,
)


class DiagnosticoService:
    def __init__(self, repositorio: PrologRepository):
        self._repo = repositorio

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

        return DiagnosticoResponse(
            sintomas_evaluados=unicos,
            fallas=fallas,
            mensaje=mensaje,
        )
