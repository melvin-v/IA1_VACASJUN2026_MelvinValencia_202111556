"""
Registro de estrategias de búsqueda disponibles.

Centralizar el registro permite que el servicio y la API descubran
algoritmos por nombre sin acoplarse a clases concretas.
"""
from typing import Dict, List

from app.algorithms.base import SearchStrategy
from app.algorithms.bfs import BFS
from app.algorithms.dfs import DFS

# Mapa nombre -> instancia de la estrategia.
_REGISTRY: Dict[str, SearchStrategy] = {
    BFS.name: BFS(),
    DFS.name: DFS(),
}


def get_strategy(name: str) -> SearchStrategy:
    """Devuelve la estrategia por nombre (case-insensitive)."""
    key = name.strip().upper()
    if key not in _REGISTRY:
        raise KeyError(
            f"Algoritmo '{name}' no soportado. "
            f"Disponibles: {', '.join(_REGISTRY.keys())}"
        )
    return _REGISTRY[key]


def available_algorithms() -> List[str]:
    """Lista de nombres de algoritmos registrados."""
    return list(_REGISTRY.keys())


__all__ = [
    "SearchStrategy",
    "BFS",
    "DFS",
    "get_strategy",
    "available_algorithms",
]
