from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from app.algorithms import available_algorithms, get_strategy
from app.domain.models import Maze, SearchResult
from app.repositories.base import MazeRepository


class MazeNotFoundError(Exception):
    """Se solicitó un laberinto que no existe en el repositorio."""


@dataclass
class ComparisonResult:
    """Comparación lado a lado de varios algoritmos sobre un mismo laberinto."""
    maze_id: str
    results: List[SearchResult]


class SearchService:
    def __init__(self, repository: MazeRepository) -> None:
        self._repo = repository

    # --------------------------- Laberintos --------------------------- #
    def list_mazes(self) -> List[Maze]:
        return self._repo.get_all()

    def get_maze(self, maze_id: str) -> Maze:
        maze = self._repo.get_by_id(maze_id)
        if maze is None:
            raise MazeNotFoundError(f"No existe el laberinto '{maze_id}'.")
        return maze

    def add_maze(self, maze: Maze) -> Maze:
        """Valida y registra un laberinto (p. ej. creado en el frontend)."""
        maze.validate()
        return self._repo.add(maze)

    # --------------------------- Búsqueda ----------------------------- #
    def run_on_maze(self, maze: Maze, algorithm: str) -> SearchResult:
        """Ejecuta un algoritmo sobre un objeto Maze ya disponible."""
        maze.validate()
        strategy = get_strategy(algorithm)
        return strategy.search(maze)

    def run(self, maze_id: str, algorithm: str) -> SearchResult:
        """Ejecuta un algoritmo sobre un laberinto del repositorio."""
        maze = self.get_maze(maze_id)
        return self.run_on_maze(maze, algorithm)

    def compare(
        self, maze_id: str, algorithms: Optional[List[str]] = None
    ) -> ComparisonResult:
        """
        Ejecuta varios algoritmos sobre el mismo laberinto y devuelve sus
        resultados para comparar ruta, nodos explorados y tiempo.
        """
        maze = self.get_maze(maze_id)
        algos = algorithms or available_algorithms()
        results = [self.run_on_maze(maze, algo) for algo in algos]
        return ComparisonResult(maze_id=maze_id, results=results)
