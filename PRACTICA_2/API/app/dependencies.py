import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    APIKeyHeader,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .repositories.usuario_repository import UsuarioRepository
from .security import decode_access_token

security_scheme = HTTPBearer()
api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(credentials.credentials)
        username = payload.get("sub")
        if username is None:
            raise error
    except jwt.PyJWTError:
        raise error

    usuario = UsuarioRepository(db).get_by_username(username)
    if usuario is None:
        raise error
    return usuario


def verify_bot_key(api_key: str = Depends(api_key_scheme)):
    if api_key != settings.bot_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clave de API inválida",
        )
    return True
