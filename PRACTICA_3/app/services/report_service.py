"""Genera reportes administrativos de facturas en CSV, Excel y PDF."""
from __future__ import annotations

import csv
import io
from typing import Sequence

from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.repositories.invoice import InvoiceRepository

CABECERAS = ["ID", "Numero", "Fecha", "Proveedor", "NIT",
             "Subtotal", "Impuestos", "Total", "Estado"]


def _fila(inv: Invoice) -> list:
    return [
        inv.id, inv.invoice_number or "", inv.invoice_date or "",
        inv.provider_name or "", inv.nit or "",
        str(inv.subtotal or ""), str(inv.taxes or ""), str(inv.total or ""),
        inv.status,
    ]


class ReportService:
    def __init__(self, db: Session):
        self.invoices = InvoiceRepository(db)

    def _datos(self) -> Sequence[Invoice]:
        return self.invoices.list(limit=10000)

    def csv_bytes(self) -> bytes:
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(CABECERAS)
        for inv in self._datos():
            w.writerow(_fila(inv))
        return buf.getvalue().encode("utf-8")

    def excel_bytes(self) -> bytes:
        wb = Workbook()
        ws = wb.active
        ws.title = "Facturas"
        ws.append(CABECERAS)
        for inv in self._datos():
            ws.append(_fila(inv))
        buf = io.BytesIO()
        wb.save(buf)
        return buf.getvalue()

    def pdf_bytes(self) -> bytes:
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=landscape(letter))
        styles = getSampleStyleSheet()
        elems = [Paragraph("Reporte de Facturas - SmartInvoice", styles["Title"]),
                 Spacer(1, 12)]
        data = [CABECERAS] + [_fila(inv) for inv in self._datos()]
        tabla = Table(data, repeatRows=1)
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#185FA5")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1EFE8")]),
        ]))
        elems.append(tabla)
        doc.build(elems)
        return buf.getvalue()
