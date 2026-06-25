from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple


class CellType(int, Enum):
    FREE = 0      # Celda transitable
    WALL = 1      # Obstáculo: bloquea el paso del agente


# Una posición es una tupla (fila, columna).
Position = Tuple[int, int]


@dataclass(frozen=True)
class Maze:
    id: str
    name: str
    grid: List[List[int]]
    start: Position
    goal: Position
    description: str = ""

    @property
    def rows(self) -> int:
        return len(self.grid)

    @property
    def cols(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    def in_bounds(self, pos: Position) -> bool:
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_wall(self, pos: Position) -> bool:
        r, c = pos
        return self.grid[r][c] == CellType.WALL

    def is_walkable(self, pos: Position) -> bool:
        return self.in_bounds(pos) and not self.is_wall(pos)

    def neighbors(self, pos: Position) -> List[Position]:
        r, c = pos
        candidates = [
            (r - 1, c),  # arriba
            (r + 1, c),  # abajo
            (r, c - 1),  # izquierda
            (r, c + 1),  # derecha
        ]
        return [p for p in candidates if self.is_walkable(p)]

    def validate(self) -> None:
        if not self.grid or not self.grid[0]:
            raise ValueError("El laberinto no puede estar vacío.")

        width = len(self.grid[0])
        if any(len(row) != width for row in self.grid):
            raise ValueError("Todas las filas deben tener el mismo ancho.")

        if not self.in_bounds(self.start):
            raise ValueError(f"La posición inicial {self.start} está fuera del laberinto.")
        if not self.in_bounds(self.goal):
            raise ValueError(f"La posición objetivo {self.goal} está fuera del laberinto.")

        if self.is_wall(self.start):
            raise ValueError("La posición inicial no puede ser un obstáculo.")
        if self.is_wall(self.goal):
            raise ValueError("La posición objetivo no puede ser un obstáculo.")


@dataclass
class SearchResult:
    algorithm: str
    found: bool
    path: List[Position] = field(default_factory=list)
    nodes_explored: int = 0
    execution_time_ms: float = 0.0
    visited_order: List[Position] = field(default_factory=list)

    @property
    def path_length(self) -> int:
        return max(len(self.path) - 1, 0)
