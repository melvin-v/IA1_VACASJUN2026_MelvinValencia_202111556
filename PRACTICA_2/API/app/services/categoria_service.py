from fastapi import HTTPException, status

from ..models import Categoria
from ..repositories.categoria_repository import CategoriaRepository


class CategoriaService:
    def __init__(self, db):
        self.repo = CategoriaRepository(db)

    def listar(self):
        return self.repo.get_all()

    def obtener(self, categoria_id):
        categoria = self.repo.get(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )
        return categoria

    def crear(self, data):
        if self.repo.get_by_nombre(data.nombre):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una categoría con ese nombre",
            )
        return self.repo.create(
            Categoria(nombre=data.nombre, descripcion=data.descripcion)
        )

    def actualizar(self, categoria_id, data):
        categoria = self.obtener(categoria_id)
        cambios = data.model_dump(exclude_unset=True)
        if "nombre" in cambios:
            existente = self.repo.get_by_nombre(cambios["nombre"])
            if existente and existente.id != categoria_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe una categoría con ese nombre",
                )
        return self.repo.update(categoria, cambios)

    def eliminar(self, categoria_id):
        categoria = self.obtener(categoria_id)
        self.repo.delete(categoria)
