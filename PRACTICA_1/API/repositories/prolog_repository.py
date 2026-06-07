import os
import re
from pyswip import Prolog
from typing import List, Optional, Tuple


_PROLOG_FILE = os.environ.get("PROLOG_FILE", "/app/prolog/rutas.pl")


class PrologRepository:
    """
    Encapsula toda comunicacion con SWI-Prolog via PySwip.
    Instancia Singleton: el archivo .pl se carga una sola vez.
    """

    _instance: Optional["PrologRepository"] = None
    _prolog: Optional[Prolog] = None

    def __new__(cls) -> "PrologRepository":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._inicializar()
        return cls._instance

    def _inicializar(self) -> None:
        self._prolog = Prolog()
        self._prolog.consult(_PROLOG_FILE)

    def obtener_ciudades(self) -> List[str]:
        resultados = list(self._prolog.query("listar_ciudades(Lista)"))
        if not resultados:
            return []
        return [str(c) for c in resultados[0]["Lista"]]

    def ciudad_existe(self, ciudad: str) -> bool:
        return bool(list(self._prolog.query(f"ciudad_existe({ciudad})")))

    def obtener_ruta_mas_corta(
        self, origen: str, destino: str
    ) -> Optional[Tuple[List[str], int]]:
        query = f"ruta_mas_corta({origen}, {destino}, Camino, Dist)"
        resultados = list(self._prolog.query(query))
        if not resultados:
            return None
        sol = resultados[0]
        camino = [str(c) for c in sol["Camino"]]
        distancia = int(sol["Dist"])
        return camino, distancia

    def obtener_todas_rutas(
        self, origen: str, destino: str
    ) -> List[Tuple[List[str], int]]:
        query = f"ruta({origen}, {destino}, [{origen}], Camino, Dist)"
        resultados = list(self._prolog.query(query))
        rutas = []
        for sol in resultados:
            camino = [str(c) for c in sol["Camino"]]
            distancia = int(sol["Dist"])
            rutas.append((camino, distancia))
        rutas.sort(key=lambda x: x[1])
        return rutas

    def agregar_ciudad(self, ciudad: str) -> bool:
        return bool(list(self._prolog.query(f"agregar_ciudad({ciudad})")))

    def agregar_conexion(self, ciudad_a: str, ciudad_b: str, distancia: int) -> bool:
        return bool(list(self._prolog.query(
            f"agregar_conexion({ciudad_a}, {ciudad_b}, {distancia})"
        )))