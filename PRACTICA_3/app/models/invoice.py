from __future__ import annotations

from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Numeric, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.enums import InvoiceStatus
from app.models.base import TimestampMixin


class Invoice(Base, TimestampMixin):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Campos extraidos por OCR (nullable: el OCR puede no encontrarlos)
    invoice_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    invoice_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    provider_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    nit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    subtotal: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    taxes: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    total: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)

    status: Mapped[str] = mapped_column(String(20), default=InvoiceStatus.PENDIENTE.value)
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey("providers.id"), nullable=True)
    uploaded_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    provider: Mapped[Optional["Provider"]] = relationship(back_populates="invoices")
    uploaded_by: Mapped[Optional["User"]] = relationship(back_populates="invoices")
    logs: Mapped[list["ProcessingLog"]] = relationship(back_populates="invoice")
