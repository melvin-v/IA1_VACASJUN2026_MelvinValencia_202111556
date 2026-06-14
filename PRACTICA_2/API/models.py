from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from .database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    preguntas = relationship(
        "Pregunta", back_populates="categoria", cascade="all, delete-orphan"
    )


class Pregunta(Base):
    __tablename__ = "preguntas"

    id = Column(Integer, primary_key=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    pregunta = Column(String(500), nullable=False)
    respuesta = Column(Text, nullable=False)
    palabras_clave = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    categoria = relationship("Categoria", back_populates="preguntas")
    consultas = relationship("Consulta", back_populates="pregunta")


class UsuarioAdmin(Base):
    __tablename__ = "usuarios_admin"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Configuracion(Base):
    __tablename__ = "configuracion"

    id = Column(Integer, primary_key=True)
    clave = Column(String(100), unique=True, nullable=False)
    valor = Column(String(255))
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True)
    pregunta_id = Column(Integer, ForeignKey("preguntas.id"), nullable=True)
    telegram_user_id = Column(BigInteger)
    telegram_username = Column(String(100))
    consulta_texto = Column(Text, nullable=False)
    respuesta_texto = Column(Text)
    respondida = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pregunta = relationship("Pregunta", back_populates="consultas")
