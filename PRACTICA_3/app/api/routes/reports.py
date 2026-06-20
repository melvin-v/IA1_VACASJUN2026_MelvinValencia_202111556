from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reportes"])

_MEDIA = {
    "csv": "text/csv",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "pdf": "application/pdf",
}


@router.get("/invoices")
def report_invoices(
    format: str = "pdf",
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    fmt = format.lower()
    if fmt not in _MEDIA:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Formato debe ser pdf, xlsx o csv")
    svc = ReportService(db)
    data = {"csv": svc.csv_bytes, "xlsx": svc.excel_bytes, "pdf": svc.pdf_bytes}[fmt]()
    return Response(
        content=data,
        media_type=_MEDIA[fmt],
        headers={"Content-Disposition": f'attachment; filename="reporte_facturas.{fmt}"'},
    )


@router.post("/invoices/email")
def email_report(
    to: str,
    format: str = "pdf",
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    from app.services.email_service import EmailService

    fmt = format.lower()
    if fmt not in _MEDIA:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Formato debe ser pdf, xlsx o csv")
    svc = ReportService(db)
    data = {"csv": svc.csv_bytes, "xlsx": svc.excel_bytes, "pdf": svc.pdf_bytes}[fmt]()
    try:
        mensaje = EmailService().send(
            to=to, subject="Reporte de Facturas - SmartInvoice",
            body="Adjunto el reporte administrativo de facturas generado por SmartInvoice.",
            attachment=data, filename=f"reporte_facturas.{fmt}", fmt=fmt,
        )
        return {"ok": True, "message": mensaje}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))
