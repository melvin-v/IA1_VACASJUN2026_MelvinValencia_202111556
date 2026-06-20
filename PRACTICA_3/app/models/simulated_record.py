from __future__ import annotations

from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class SimulatedRecord(Base, TimestampMixin):
    """Registros creados por el RPA en el 'sistema externo simulado'."""
    __tablename__ = "simulated_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    invoice_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    provider_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    nit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    total: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    source: Mapped[str] = mapped_column(String(20), default="RPA")
