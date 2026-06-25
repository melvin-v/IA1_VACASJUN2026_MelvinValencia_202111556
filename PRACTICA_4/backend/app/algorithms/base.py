"""
Strategy Pattern para los algoritmos de búsqueda.

Cada algoritmo (BFS, DFS, y opcionalmente A*) implementa la misma interfaz
`SearchStrategy.search(...)`. Esto permite que el servicio ejecute cualquier
algoritmo sin conocer su implementación interna, y facilita agregar nuevos.
"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from app.domain.models import Maze, Position, SearchResult


class SearchStrategy(ABC):
    """Interfaz común a todos los algoritmos de búsqueda."""

    #: Nombre legible del algoritmo (se usa en la respuesta de la API).
    name: str = "base"

    @abstractmethod
    def search(self, maze: Maze) -> SearchResult:
        """Ejecuta la búsqueda sobre el laberinto y devuelve un SearchResult."""
        raise NotImplementedError

    # ----------------------------------------------------------------- #
    # Utilidades compartidas por las estrategias concretas
    # ----------------------------------------------------------------- #
    @staticmethod
    def reconstruct_path(
        came_from: Dict[Position, Optional[Position]],
        start: Position,
        goal: Position,
    ) -> List[Position]:
        """
        Reconstruye la ruta desde `goal` hasta `start` usando el mapa de
        predecesores `came_from`, y la devuelve en orden start -> goal.
        """
        path: List[Position] = []
        current: Optional[Position] = goal
        while current is not None:
            path.append(current)
            if current == start:
                break
            current = came_from.get(current)
        path.reverse()
        return path

    @staticmethod
    def _now_ms() -> float:
        """Reloj monotónico de alta resolución, en milisegundos."""
        return time.perf_counter() * 1000.0
