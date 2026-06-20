"""Valida los campos extraidos y decide el estado de la factura."""
from __future__ import annotations

from decimal import Decimal
from typing import Optional

from app.core.enums import InvoiceStatus

TOLERANCIA = Decimal("0.05")


class InvoiceValidator:
    def validate(self, fields: dict) -> tuple[str, list[str]]:
        errores: list[str] = []

        if not fields.get("invoice_number"):
            errores.append("No se detecto el numero de factura")
        if fields.get("total") is None:
            errores.append("No se detecto el total")
        if not fields.get("nit"):
            errores.append("No se detecto el NIT del proveedor")

        st: Optional[Decimal] = fields.get("subtotal")
        tx: Optional[Decimal] = fields.get("taxes")
        tot: Optional[Decimal] = fields.get("total")
        if st is not None and tx is not None and tot is not None:
            if abs((st + tx) - tot) > TOLERANCIA:
                errores.append("Subtotal + impuestos no coincide con el total")

        # Decision de estado
        nada_extraido = fields.get("total") is None and not fields.get("invoice_number")
        if not errores:
            estado = InvoiceStatus.PROCESADO.value
        elif nada_extraido:
            estado = InvoiceStatus.ERROR.value       # OCR no extrajo nada util
        else:
            estado = InvoiceStatus.RECHAZADO.value   # extraido pero incompleto/inconsistente
        return estado, errores
