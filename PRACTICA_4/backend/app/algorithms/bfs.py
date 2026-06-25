"""
Breadth-First Search (BFS) — búsqueda en anchura.

Explora el laberinto por niveles usando una cola FIFO. Como cada arista
tiene el mismo costo (un paso), BFS garantiza encontrar la ruta MÁS CORTA
en número de pasos. Implementado a mano: solo se usa `deque` como cola,
no librerías de pathfinding.
"""
from __future__ import annotations

from collections import deque
from typing import Dict, Optional

from app.algorithms.base import SearchStrategy
from app.domain.models import Maze, Position, SearchResult


class BFS(SearchStrategy):
    name = "BFS"

    def search(self, maze: Maze) -> SearchResult:
        start = maze.start
        goal = maze.goal

        start_time = self._now_ms()

        # Cola de posiciones por visitar (FIFO -> búsqueda en anchura).
        frontier: deque[Position] = deque([start])
        # Predecesor de cada nodo para reconstruir la ruta al final.
        came_from: Dict[Position, Optional[Position]] = {start: None}
        # Orden en que se expanden los nodos (para animación y conteo).
        visited_order: list[Position] = []
        nodes_explored = 0

        while frontier:
            current = frontier.popleft()
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

            for neighbor in maze.neighbors(current):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    frontier.append(neighbor)

        # Frontera agotada sin encontrar la meta: no existe ruta.
        return SearchResult(
            algorithm=self.name,
            found=False,
            path=[],
            nodes_explored=nodes_explored,
            execution_time_ms=self._now_ms() - start_time,
            visited_order=visited_order,
        )
