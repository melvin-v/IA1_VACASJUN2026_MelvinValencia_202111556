from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, db: Session):
        self.users = UserRepository(db)

    def register(self, data: UserCreate) -> User:
        if self.users.get_by_email(data.email):
            raise ValueError("El email ya esta registrado")
        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
        )
        return self.users.add(user)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.users.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def login_token(self, user: User) -> str:
        return create_access_token(subject=user.email)
