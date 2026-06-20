from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.provider import Provider
from app.repositories.base import BaseRepository


class ProviderRepository(BaseRepository[Provider]):
    def __init__(self, db: Session):
        super().__init__(Provider, db)

    def get_by_nit(self, nit: str) -> Optional[Provider]:
        stmt = select(Provider).where(Provider.nit == nit)
        return self.db.execute(stmt).scalar_one_or_none()
