from typing import Optional, Sequence

from sqlalchemy.orm import Session

from app.models.provider import Provider
from app.repositories.provider import ProviderRepository
from app.schemas.provider import ProviderCreate, ProviderUpdate


class ProviderService:
    def __init__(self, db: Session):
        self.repo = ProviderRepository(db)

    def create(self, data: ProviderCreate) -> Provider:
        if self.repo.get_by_nit(data.nit):
            raise ValueError("Ya existe un proveedor con ese NIT")
        provider = Provider(**data.model_dump())
        return self.repo.add(provider)

    def get(self, provider_id: int) -> Optional[Provider]:
        return self.repo.get(provider_id)

    def list(self, skip: int = 0, limit: int = 100) -> Sequence[Provider]:
        return self.repo.list(skip=skip, limit=limit)

    def update(self, provider_id: int, data: ProviderUpdate) -> Optional[Provider]:
        provider = self.repo.get(provider_id)
        if not provider:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(provider, field, value)
        return self.repo.update(provider)

    def delete(self, provider_id: int) -> bool:
        provider = self.repo.get(provider_id)
        if not provider:
            return False
        self.repo.delete(provider)
        return True
