"""
Schemas Pydantic (capa de transporte de la API REST).

Separan el formato JSON que viaja por HTTP de los modelos de dominio.
En JSON una posición es una lista [fila, columna]; en el dominio es una
tupla. Los mappers de este módulo hacen la conversión en ambos sentidos.
"""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from app.domain.models import Maze, SearchResult

# Una posición en JSON viaja como [fila, columna].
PositionSchema = List[int]


# --------------------------- Laberinto ------------------------------ #
class MazeSchema(BaseModel):
    """Laberinto tal como viaja por la API."""
    id: str = Field(..., examples=["custom_1"])
    name: str = Field(..., examples=["Mi laberinto"])
    description: str = ""
    grid: List[List[int]] = Field(
        ..., description="Cuadrícula: 0 = libre, 1 = obstáculo."
    )
    start: PositionSchema = Field(..., examples=[[0, 0]])
    goal: PositionSchema = Field(..., examples=[[4, 4]])

    @classmethod
    def from_domain(cls, maze: Maze) -> "MazeSchema":
        return cls(
            id=maze.id,
            name=maze.name,
            description=maze.description,
            grid=[list(row) for row in maze.grid],
            start=list(maze.start),
            goal=list(maze.goal),
        )

    def to_domain(self) -> Maze:
        return Maze(
            id=self.id,
            name=self.name,
            description=self.description,
            grid=[list(row) for row in self.grid],
            start=(self.start[0], self.start[1]),
            goal=(self.goal[0], self.goal[1]),
        )


# --------------------------- Resultado ------------------------------ #
class SearchResultSchema(BaseModel):
    """Resultado de una búsqueda tal como viaja por la API."""
    algorithm: str
    found: bool
    path: List[PositionSchema]
    path_length: int
    nodes_explored: int
    execution_time_ms: float
    visited_order: List[PositionSchema]

    @classmethod
    def from_domain(cls, result: SearchResult) -> "SearchResultSchema":
        return cls(
            algorithm=result.algorithm,
            found=result.found,
            path=[list(p) for p in result.path],
            path_length=result.path_length,
            nodes_explored=result.nodes_explored,
            execution_time_ms=round(result.execution_time_ms, 4),
            visited_order=[list(p) for p in result.visited_order],
        )


# --------------------------- Requests ------------------------------- #
class SearchRequest(BaseModel):
    """
    Petición de búsqueda. El laberinto viaja en el cuerpo, de modo que el
    frontend puede enviar tanto un laberinto predefinido como uno dibujado
    por el usuario.
    """
    maze: MazeSchema
    algorithm: str = Field(..., examples=["BFS"])


class CompareRequest(BaseModel):
    """Petición de comparación entre varios algoritmos sobre un laberinto."""
    maze: MazeSchema
    algorithms: Optional[List[str]] = Field(
        default=None,
        description="Lista de algoritmos a comparar. Si se omite, usa todos.",
        examples=[["BFS", "DFS"]],
    )


class CompareResponse(BaseModel):
    """Resultados de la comparación, uno por algoritmo."""
    maze_id: str
    results: List[SearchResultSchema]


# --------------------------- Misc ----------------------------------- #
class AlgorithmsResponse(BaseModel):
    algorithms: List[str]


class ErrorResponse(BaseModel):
    detail: str
