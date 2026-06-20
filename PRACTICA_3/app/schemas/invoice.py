from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class InvoiceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    provider_name: Optional[str] = None
    nit: Optional[str] = None
    subtotal: Optional[Decimal] = None
    taxes: Optional[Decimal] = None
    total: Optional[Decimal] = None
    status: str
    provider_id: Optional[int] = None
    created_at: Optional[datetime] = None
