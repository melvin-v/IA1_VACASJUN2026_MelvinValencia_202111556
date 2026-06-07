from fastapi import APIRouter
from models.schemas import NuevaCiudad, NuevaConexion
from services.rutas_service import RutasService

router = APIRouter(prefix="/api", tags=["Rutas Guatemala"])
service = RutasService()


@router.get("/ciudades")
def listar_ciudades():
    return service.listar_ciudades()


@router.get("/ruta/corta")
def ruta_mas_corta(origen: str, destino: str):
    return service.obtener_ruta_mas_corta(origen, destino)


@router.get("/ruta/todas")
def todas_las_rutas(origen: str, destino: str):
    return service.obtener_todas_rutas(origen, destino)


@router.post("/ciudades")
def agregar_ciudad(datos: NuevaCiudad):
    return service.agregar_ciudad(datos)


@router.post("/conexiones")
def agregar_conexion(datos: NuevaConexion):
    return service.agregar_conexion(datos)