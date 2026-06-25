from typing import List

from app.domain.models import Maze


def _build_seed_mazes() -> List[Maze]:
    return [
        Maze(
            id="basico_5x5",
            name="Laberinto Básico 5x5",
            description="Camino corto con un par de muros. Ideal para empezar.",
            start=(0, 0),
            goal=(4, 4),
            grid=[
                [0, 0, 1, 0, 0],
                [1, 0, 1, 0, 1],
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
            ],
        ),
        Maze(
            id="serpiente_7x7",
            name="Serpiente 7x7",
            description="Pasillos largos en zigzag que obligan a recorrer casi todo el mapa.",
            start=(0, 0),
            goal=(6, 6),
            grid=[
                [0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0],
            ],
        ),
        Maze(
            id="abierto_8x8",
            name="Campo Abierto 8x8",
            description="Pocos obstáculos: BFS y DFS toman rutas muy distintas.",
            start=(0, 0),
            goal=(7, 7),
            grid=[
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 1, 1, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [1, 1, 0, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 1, 0],
                [0, 1, 1, 1, 1, 0, 1, 0],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 1, 1, 0, 0, 0],
            ],
        ),
        Maze(
            id="zigzag_10x10",
            name="Zigzag 10x10",
            description="Laberinto grande tipo serpiente para comparar rendimiento.",
            start=(0, 0),
            goal=(9, 9),
            grid=[
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            ],
        ),
        Maze(
            id="sin_salida_6x6",
            name="Sin Salida 6x6",
            description="La meta está encerrada por muros: NO existe ruta válida.",
            start=(0, 0),
            goal=(5, 5),
            grid=[
                [0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 1],
                [0, 1, 0, 0, 0, 1],
                [0, 1, 0, 0, 1, 1],
                [0, 0, 0, 0, 1, 0],
            ],
        ),
    ]


SEED_MAZES: List[Maze] = _build_seed_mazes()
