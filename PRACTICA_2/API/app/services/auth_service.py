from fastapi import HTTPException, status

from ..repositories.usuario_repository import UsuarioRepository
from ..security import create_access_token, verify_password


class AuthService:
    def __init__(self, db):
        self.repo = UsuarioRepository(db)

    def autenticar(self, username, password):
        usuario = self.repo.get_by_username(username)
        if not usuario or not verify_password(password, usuario.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )
        return create_access_token({"sub": usuario.username})
