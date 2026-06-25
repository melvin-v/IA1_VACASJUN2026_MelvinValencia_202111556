from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.models import Maze


class MazeRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Maze]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, maze_id: str) -> Optional[Maze]:
        raise NotImplementedError

    @abstractmethod
    def add(self, maze: Maze) -> Maze:
        raise NotImplementedError
