from fastapi import HTTPException
from typing import List

from repositories.prolog_repository import PrologRepository
from models.schemas import (
    RutaResponse, RutaMasCorta, TodasLasRutas,
    CiudadesResponse, MensajeResponse, NuevaCiudad, NuevaConexion,
)


class RutasService:

    def __init__(self):
        self.repo = PrologRepository()

    def _validar_ciudad(self, nombre: str) -> None:
        if not self.repo.ciudad_existe(nombre):
            raise HTTPException(
                status_code=404,
                detail=f"La ciudad '{nombre}' no existe en la base de conocimiento.",
            )

    def _validar_origen_destino(self, origen: str, destino: str) -> None:
        if origen == destino:
            raise HTTPException(
                status_code=400,
                detail="El origen y el destino no pueden ser la misma ciudad.",
            )
        self._validar_ciudad(origen)
        self._validar_ciudad(destino)

    def _construir_ruta_response(self, camino: List[str], distancia: int) -> RutaResponse:
        return RutaResponse(
            camino=camino,
            distancia_km=distancia,
            num_paradas=len(camino),
        )

    def listar_ciudades(self) -> CiudadesResponse:
        ciudades = sorted(self.repo.obtener_ciudades())
        return CiudadesResponse(ciudades=ciudades, total=len(ciudades))

    def obtener_ruta_mas_corta(self, origen: str, destino: str) -> RutaMasCorta:
        self._validar_origen_destino(origen, destino)

        resultado = self.repo.obtener_ruta_mas_corta(origen, destino)
        if resultado is None:
            raise HTTPException(
                status_code=404,
                detail=f"No existe ninguna ruta entre '{origen}' y '{destino}'.",
            )

        camino, distancia = resultado
        return RutaMasCorta(
            origen=origen,
            destino=destino,
            ruta=self._construir_ruta_response(camino, distancia),
            mensaje="Ruta mas corta encontrada exitosamente.",
        )

    def obtener_todas_rutas(self, origen: str, destino: str) -> TodasLasRutas:
        self._validar_origen_destino(origen, destino)

        rutas_raw = self.repo.obtener_todas_rutas(origen, destino)
        if not rutas_raw:
            raise HTTPException(
                status_code=404,
                detail=f"No existe ninguna ruta entre '{origen}' y '{destino}'.",
            )

        rutas = [self._construir_ruta_response(c, d) for c, d in rutas_raw]
        return TodasLasRutas(
            origen=origen,
            destino=destino,
            total_rutas=len(rutas),
            rutas=rutas,
        )

    def agregar_ciudad(self, datos: NuevaCiudad) -> MensajeResponse:
        if self.repo.ciudad_existe(datos.nombre):
            return MensajeResponse(
                exito=False,
                mensaje=f"La ciudad '{datos.nombre}' ya existe.",
            )
        self.repo.agregar_ciudad(datos.nombre)
        return MensajeResponse(
            exito=True,
            mensaje=f"Ciudad '{datos.nombre}' agregada exitosamente.",
        )

    def agregar_conexion(self, datos: NuevaConexion) -> MensajeResponse:
        self._validar_ciudad(datos.ciudad_a)
        self._validar_ciudad(datos.ciudad_b)

        if datos.ciudad_a == datos.ciudad_b:
            raise HTTPException(
                status_code=400,
                detail="No se puede conectar una ciudad consigo misma.",
            )

        self.repo.agregar_conexion(datos.ciudad_a, datos.ciudad_b, datos.distancia_km)
        return MensajeResponse(
            exito=True,
            mensaje=(
                f"Conexion entre '{datos.ciudad_a}' y '{datos.ciudad_b}' "
                f"({datos.distancia_km} km) agregada exitosamente."
            ),
        )