import json
import os
import threading

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_RUTA_DEFECTO = os.path.normpath(
    os.path.join(_BASE_DIR, "..", "..", "data", "historial.json")
)


class HistorialRepository:
    def __init__(self, ruta: str = _RUTA_DEFECTO):
        self._ruta = ruta
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(self._ruta), exist_ok=True)

    def _leer(self) -> list:
        if not os.path.exists(self._ruta):
            return []
        try:
            with open(self._ruta, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []

    def _escribir(self, datos: list) -> None:
        with open(self._ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def guardar(self, registro: dict) -> dict:
        with self._lock:
            datos = self._leer()
            datos.append(registro)
            self._escribir(datos)
        return registro

    def listar(self, limite: int | None = None) -> list:
        with self._lock:
            datos = self._leer()
        datos = list(reversed(datos))
        if limite is not None and limite > 0:
            datos = datos[:limite]
        return datos
