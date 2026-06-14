from fastapi import HTTPException, status

from ..models import Configuracion
from ..repositories.configuracion_repository import ConfiguracionRepository


class ConfiguracionService:
    def __init__(self, db):
        self.repo = ConfiguracionRepository(db)

    def listar(self):
        return self.repo.get_all()

    def obtener(self, clave):
        configuracion = self.repo.get_by_clave(clave)
        if not configuracion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Configuración no encontrada",
            )
        return configuracion

    def actualizar(self, clave, valor):
        configuracion = self.repo.get_by_clave(clave)
        if configuracion:
            return self.repo.update(configuracion, {"valor": valor})
        return self.repo.create(Configuracion(clave=clave, valor=valor))

    def valor(self, clave, default=None):
        configuracion = self.repo.get_by_clave(clave)
        if configuracion and configuracion.valor:
            return configuracion.valor
        return default
