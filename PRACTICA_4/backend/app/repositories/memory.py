from __future__ import annotations

from typing import Dict, List, Optional

from app.domain.models import Maze
from app.repositories.base import MazeRepository
from app.repositories.seed import SEED_MAZES


class InMemoryMazeRepository(MazeRepository):

    def __init__(self, seed: bool = True) -> None:
        self._store: Dict[str, Maze] = {}
        if seed:
            for maze in SEED_MAZES:
                self._store[maze.id] = maze

    def get_all(self) -> List[Maze]:
        return list(self._store.values())

    def get_by_id(self, maze_id: str) -> Optional[Maze]:
        return self._store.get(maze_id)

    def add(self, maze: Maze) -> Maze:
        self._store[maze.id] = maze
        return maze
