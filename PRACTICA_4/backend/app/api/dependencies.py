from functools import lru_cache

from app.repositories.memory import InMemoryMazeRepository
from app.services.search_service import SearchService


@lru_cache(maxsize=1)
def get_repository() -> InMemoryMazeRepository:
    return InMemoryMazeRepository()


def get_search_service() -> SearchService:
    return SearchService(get_repository())
