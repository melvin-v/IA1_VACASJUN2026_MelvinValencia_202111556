from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class ProcessingLog(Base, TimestampMixin):
    """Bitacora: historial de cada documento procesado."""
    __tablename__ = "processing_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20))
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    invoice_id: Mapped[Optional[int]] = mapped_column(ForeignKey("invoices.id"), nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    invoice: Mapped[Optional["Invoice"]] = relationship(back_populates="logs")
    user: Mapped[Optional["User"]] = relationship(back_populates="logs")
