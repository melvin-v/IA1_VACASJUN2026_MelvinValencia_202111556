import os
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.invoice import InvoiceRead
from app.services.invoice_service import InvoiceService, save_upload

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("/upload", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def upload_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ext = os.path.splitext(file.filename or "")[1].lower().lstrip(".")
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato no permitido. Use: {', '.join(sorted(settings.ALLOWED_EXTENSIONS))}",
        )
    content = file.file.read()
    path = save_upload(content, file.filename or f"factura.{ext}")
    try:
        return InvoiceService(db).process(path, file.filename or "factura", current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"No se pudo procesar la factura: {e}",
        )


@router.get("", response_model=List[InvoiceRead])
def list_invoices(
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return InvoiceService(db).list(status=status_filter, skip=skip, limit=limit)


@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    inv = InvoiceService(db).get(invoice_id)
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
    return inv


@router.post("/{invoice_id}/rpa")
def run_rpa(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from app.models.processing_log import ProcessingLog
    from app.repositories.processing_log import ProcessingLogRepository
    from app.services.rpa_service import RPAService

    svc = InvoiceService(db)
    inv = svc.get(invoice_id)
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
    try:
        mensaje = RPAService().register_invoice(inv)
        ProcessingLogRepository(db).add(ProcessingLog(
            invoice_id=inv.id, user_id=current_user.id,
            document_name=inv.invoice_number or f"factura-{inv.id}",
            status="PROCESADO", result=f"RPA: {mensaje}",
        ))
        return {"ok": True, "message": mensaje}
    except Exception as e:
        ProcessingLogRepository(db).add(ProcessingLog(
            invoice_id=inv.id, user_id=current_user.id,
            document_name=inv.invoice_number or f"factura-{inv.id}",
            status="ERROR", result=f"RPA fallo: {e}",
        ))
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"RPA falló: {e}")
