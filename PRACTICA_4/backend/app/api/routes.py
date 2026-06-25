from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.algorithms import available_algorithms
from app.api.dependencies import get_search_service
from app.schemas import (
    AlgorithmsResponse,
    CompareRequest,
    CompareResponse,
    MazeSchema,
    SearchRequest,
    SearchResultSchema,
)
from app.services.search_service import MazeNotFoundError, SearchService

router = APIRouter(prefix="/api", tags=["robomaze"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "RoboMaze API"}


@router.get("/algorithms", response_model=AlgorithmsResponse)
def list_algorithms() -> AlgorithmsResponse:
    return AlgorithmsResponse(algorithms=available_algorithms())


@router.get("/mazes", response_model=list[MazeSchema])
def list_mazes(
    service: SearchService = Depends(get_search_service),
) -> list[MazeSchema]:
    return [MazeSchema.from_domain(m) for m in service.list_mazes()]


@router.get("/mazes/{maze_id}", response_model=MazeSchema)
def get_maze(
    maze_id: str,
    service: SearchService = Depends(get_search_service),
) -> MazeSchema:
    try:
        maze = service.get_maze(maze_id)
    except MazeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    return MazeSchema.from_domain(maze)


@router.post("/search", response_model=SearchResultSchema)
def search(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service),
) -> SearchResultSchema:
    maze = request.maze.to_domain()
    try:
        maze.validate()
    except ValueError as exc:
        raise HTTPException(
            status_code=422, detail=str(exc)
        ) from exc

    try:
        result = service.run_on_maze(maze, request.algorithm)
    except KeyError as exc:
        # Algoritmo no soportado.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.args[0]
        ) from exc

    return SearchResultSchema.from_domain(result)


@router.post("/compare", response_model=CompareResponse)
def compare(
    request: CompareRequest,
    service: SearchService = Depends(get_search_service),
) -> CompareResponse:
    maze = request.maze.to_domain()
    try:
        maze.validate()
    except ValueError as exc:
        raise HTTPException(
            status_code=422, detail=str(exc)
        ) from exc

    algos = request.algorithms or available_algorithms()
    try:
        results = [service.run_on_maze(maze, a) for a in algos]
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.args[0]
        ) from exc

    return CompareResponse(
        maze_id=maze.id,
        results=[SearchResultSchema.from_domain(r) for r in results],
    )
