import re
import unicodedata

from fastapi import HTTPException, status

from ..models import Pregunta
from ..repositories.categoria_repository import CategoriaRepository
from ..repositories.pregunta_repository import PreguntaRepository

STOPWORDS = {
    "que",
    "cual",
    "cuales",
    "como",
    "cuando",
    "donde",
    "para",
    "por",
    "con",
    "los",
    "las",
    "una",
    "unos",
    "unas",
    "del",
    "puedo",
    "necesito",
    "tengo",
    "hay",
    "sobre",
    "este",
    "esta",
    "mas",
}


def _normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    return texto


def _tokens(texto):
    return [
        t
        for t in _normalizar(texto).split()
        if len(t) > 2 and t not in STOPWORDS
    ]


class PreguntaService:
    def __init__(self, db):
        self.repo = PreguntaRepository(db)
        self.categorias = CategoriaRepository(db)

    def listar(self):
        return self.repo.get_all()

    def obtener(self, pregunta_id):
        pregunta = self.repo.get(pregunta_id)
        if not pregunta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pregunta no encontrada",
            )
        return pregunta

    def _validar_categoria(self, categoria_id):
        if not self.categorias.get(categoria_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La categoría indicada no existe",
            )

    def crear(self, data):
        self._validar_categoria(data.categoria_id)
        return self.repo.create(
            Pregunta(
                categoria_id=data.categoria_id,
                pregunta=data.pregunta,
                respuesta=data.respuesta,
                palabras_clave=data.palabras_clave,
            )
        )

    def actualizar(self, pregunta_id, data):
        pregunta = self.obtener(pregunta_id)
        cambios = data.model_dump(exclude_unset=True)
        if "categoria_id" in cambios:
            self._validar_categoria(cambios["categoria_id"])
        return self.repo.update(pregunta, cambios)

    def eliminar(self, pregunta_id):
        pregunta = self.obtener(pregunta_id)
        self.repo.delete(pregunta)

    def buscar_respuesta(self, texto):
        tokens = set(_tokens(texto))
        if not tokens:
            return None

        mejor = None
        mejor_score = 0
        for pregunta in self.repo.get_all():
            contenido = _normalizar(
                f"{pregunta.pregunta} {pregunta.palabras_clave or ''}"
            )
            palabras = set(contenido.split())
            score = len(tokens & palabras)
            if score > mejor_score:
                mejor_score = score
                mejor = pregunta

        return mejor if mejor_score > 0 else None
