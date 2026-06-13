import os
import threading

from pyswip import Prolog

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_PROLOG_FILE = os.path.normpath(
    os.path.join(_BASE_DIR, "..", "..", "prolog", "doctor_byte.pl")
)


class PrologRepository:

    def __init__(self, prolog_file: str = _PROLOG_FILE):
        self._prolog = Prolog()
        self._lock = threading.Lock()
        self._prolog.consult(prolog_file.replace("\\", "/"))

    def listar_sintomas(self) -> list[dict]:
        with self._lock:
            soluciones = list(self._prolog.query("sintoma(Id, Desc)"))
        return [
            {"id": str(s["Id"]), "descripcion": str(s["Desc"])}
            for s in soluciones
        ]

    def diagnosticar(self, sintomas: list[str]) -> list[str]:
        lista_prolog = ", ".join(sintomas)
        consulta = f"diagnosticar([{lista_prolog}], Fallas)"
        with self._lock:
            soluciones = list(self._prolog.query(consulta))
        if not soluciones:
            return []
        return [str(f) for f in soluciones[0]["Fallas"]]

    def obtener_falla(self, id_falla: str) -> dict | None:
        with self._lock:
            desc = list(self._prolog.query(f"falla({id_falla}, Desc)"))
            rec = list(self._prolog.query(f"recomendacion({id_falla}, Rec)"))
        if not desc:
            return None
        return {
            "id": id_falla,
            "descripcion": str(desc[0]["Desc"]),
            "recomendacion": str(rec[0]["Rec"]) if rec else "",
        }
