from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.repositories.base import BaseRepository


class InvoiceRepository(BaseRepository[Invoice]):
    def __init__(self, db: Session):
        super().__init__(Invoice, db)

    def list_by_status(self, status: str, skip: int = 0, limit: int = 100) -> Sequence[Invoice]:
        stmt = select(Invoice).where(Invoice.status == status).offset(skip).limit(limit)
        return self.db.execute(stmt).scalars().all()

    def get_by_number(self, invoice_number: str) -> Optional[Invoice]:
        stmt = select(Invoice).where(Invoice.invoice_number == invoice_number)
        return self.db.execute(stmt).scalars().first()
