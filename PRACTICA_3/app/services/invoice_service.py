"""Orquesta el procesamiento de una factura de punta a punta."""
from __future__ import annotations

import os
import uuid
from typing import Optional, Sequence

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.enums import InvoiceStatus
from app.models.invoice import Invoice
from app.models.processing_log import ProcessingLog
from app.models.user import User
from app.repositories.invoice import InvoiceRepository
from app.repositories.processing_log import ProcessingLogRepository
from app.repositories.provider import ProviderRepository
from app.services.invoice_parser import InvoiceParser
from app.services.invoice_validator import InvoiceValidator
from app.services.ocr_service import OCRService


def save_upload(content: bytes, original_name: str) -> str:
    """Guarda el archivo subido con un nombre unico y devuelve la ruta."""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(original_name)[1].lower()
    path = os.path.join(settings.UPLOAD_DIR, f"{uuid.uuid4().hex}{ext}")
    with open(path, "wb") as f:
        f.write(content)
    return path


class InvoiceService:
    def __init__(self, db: Session):
        self.db = db
        self.invoices = InvoiceRepository(db)
        self.logs = ProcessingLogRepository(db)
        self.providers = ProviderRepository(db)
        self.ocr = OCRService()
        self.parser = InvoiceParser()
        self.validator = InvoiceValidator()

    def process(self, file_path: str, original_name: str, user: User) -> Invoice:
        try:
            text = self.ocr.extract_text(file_path)
            fields = self.parser.parse(text)
            estado, errores = self.validator.validate(fields)

            # vincular proveedor existente por NIT (si lo hay)
            provider = self.providers.get_by_nit(fields["nit"]) if fields.get("nit") else None

            invoice = Invoice(
                invoice_number=fields["invoice_number"],
                invoice_date=fields["invoice_date"],
                provider_name=fields["provider_name"],
                nit=fields["nit"],
                subtotal=fields["subtotal"],
                taxes=fields["taxes"],
                total=fields["total"],
                status=estado,
                file_path=file_path,
                raw_text=text,
                provider_id=provider.id if provider else None,
                uploaded_by_id=user.id,
            )
            invoice = self.invoices.add(invoice)

            resultado = "Procesada correctamente" if not errores else "; ".join(errores)
            self._log(invoice.id, user.id, original_name, estado, resultado)
            return invoice
        except Exception as e:
            self._log(None, user.id, original_name, InvoiceStatus.ERROR.value,
                      f"Error de procesamiento: {e}")
            raise

    def _log(self, invoice_id, user_id, document_name, status, result):
        self.logs.add(ProcessingLog(
            invoice_id=invoice_id, user_id=user_id,
            document_name=document_name, status=status, result=result,
        ))

    # consultas
    def get(self, invoice_id: int) -> Optional[Invoice]:
        return self.invoices.get(invoice_id)

    def list(self, status: Optional[str] = None, skip: int = 0, limit: int = 100) -> Sequence[Invoice]:
        if status:
            return self.invoices.list_by_status(status, skip=skip, limit=limit)
        return self.invoices.list(skip=skip, limit=limit)
