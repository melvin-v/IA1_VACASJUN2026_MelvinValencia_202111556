"""
Depth-First Search (DFS) — búsqueda en profundidad.

Explora tan profundo como puede por una rama antes de retroceder, usando
una pila LIFO. NO garantiza la ruta más corta, pero suele expandir menos
nodos en algunos laberintos. Implementado a mano con una lista como pila.
"""
from __future__ import annotations

from typing import Dict, Optional

from app.algorithms.base import SearchStrategy
from app.domain.models import Maze, Position, SearchResult


class DFS(SearchStrategy):
    name = "DFS"

    def search(self, maze: Maze) -> SearchResult:
        start = maze.start
        goal = maze.goal

        start_time = self._now_ms()

        # Pila de posiciones por visitar (LIFO -> búsqueda en profundidad).
        frontier: list[Position] = [start]
        came_from: Dict[Position, Optional[Position]] = {start: None}
        visited: set[Position] = set()
        visited_order: list[Position] = []
        nodes_explored = 0

        while frontier:
            current = frontier.pop()

            # Un nodo puede entrar a la pila varias veces; lo procesamos
            # solo la primera vez que sale.
            if current in visited:
                continue
            visited.add(current)
            visited_order.append(current)
            nodes_explored += 1

            if current == goal:
                path = self.reconstruct_path(came_from, start, goal)
                return SearchResult(
                    algorithm=self.name,
                    found=True,
                    path=path,
                    nodes_explored=nodes_explored,
                    execution_time_ms=self._now_ms() - start_time,
                    visited_order=visited_order,
                )

            # Se apilan los vecinos en orden inverso para que el primer
            # vecino (arriba) se procese primero al hacer pop.
            for neighbor in reversed(maze.neighbors(current)):
                if neighbor not in visited:
                    # Registramos el predecesor solo si aún no tiene uno,
                    # para no sobrescribir el camino ya trazado.
                    if neighbor not in came_from:
                        came_from[neighbor] = current
                    frontier.append(neighbor)

        return SearchResult(
            algorithm=self.name,
            found=False,
            path=[],
            nodes_explored=nodes_explored,
            execution_time_ms=self._now_ms() - start_time,
            visited_order=visited_order,
        )
