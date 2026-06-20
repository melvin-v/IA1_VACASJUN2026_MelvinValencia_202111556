"""Extrae los campos de una factura a partir del texto OCR.

Usa heuristicas/regex pensadas para facturas de Guatemala (NIT, IVA 12%,
fechas dd/mm/aaaa, montos con 'Q'). El OCR no es perfecto, asi que cualquier
campo puede salir como None y eso lo maneja el validador.
"""
from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Optional


def _to_decimal(raw: str) -> Optional[Decimal]:
    s = re.sub(r"[^\d.,]", "", raw)
    if not s:
        return None
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):      # 1.234,56 -> coma decimal
            s = s.replace(".", "").replace(",", ".")
        else:                                 # 1,234.56 -> coma miles
            s = s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".") if re.search(r",\d{2}$", s) else s.replace(",", "")
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


class InvoiceParser:
    def parse(self, text: str) -> dict:
        return {
            "invoice_number": self._invoice_number(text),
            "invoice_date": self._date(text),
            "nit": self._nit(text),
            "provider_name": self._provider_name(text),
            "subtotal": self._amount(text, [r"sub\s*-?\s*total"]),
            "taxes": self._amount(text, [r"i\.?v\.?a\.?", r"impuestos?"]),
            "total": self._amount(text, [r"(?<!sub)(?<!sub )total\s+a\s+pagar", r"(?<!sub)(?<!sub )gran\s+total", r"(?<!sub)(?<!sub-)(?<!sub )total"]),
        }

    # ---- campos de texto ----
    def _invoice_number(self, text: str) -> Optional[str]:
        patrones = [
            r"(?:n[uú]mero\s+de\s+factura|factura\s+n[o°.]*|no\.?\s*factura|serie\s*y\s*n[uú]mero|dte)\s*[:#\-]?\s*([A-Za-z0-9][A-Za-z0-9\-]{2,})",
            r"factura\s*[:#\-]?\s*([A-Za-z0-9][A-Za-z0-9\-]{3,})",
        ]
        for p in patrones:
            m = re.search(p, text, re.IGNORECASE)
            if m:
                return m.group(1).strip()
        return None

    def _date(self, text: str) -> Optional[str]:
        m = re.search(r"(\d{1,2}[/\-.]\d{1,2}[/\-.]\d{2,4})", text)
        return m.group(1) if m else None

    def _nit(self, text: str) -> Optional[str]:
        m = re.search(r"nit\s*[:\-]?\s*([0-9][0-9\-]{3,}[0-9kK])", text, re.IGNORECASE)
        return m.group(1).strip() if m else None

    def _provider_name(self, text: str) -> Optional[str]:
        """Heuristica: primera linea 'de texto' (no numeros/fechas) del encabezado."""
        for linea in text.splitlines():
            l = linea.strip()
            if len(l) < 4:
                continue
            letras = sum(c.isalpha() for c in l)
            if letras >= len(l) * 0.5 and not re.search(r"factura|nit|fecha", l, re.IGNORECASE):
                return l[:255]
        return None

    # ---- montos ----
    def _amount(self, text: str, labels: list[str]) -> Optional[Decimal]:
        for linea in text.splitlines():
            if any(re.search(lb, linea, re.IGNORECASE) for lb in labels):
                limpia = re.sub(r"\d+\s*%", "", linea)        # elimina "12%"
                numeros = re.findall(r"[\d.,]*\d", limpia)
                valores = [v for v in (_to_decimal(n) for n in numeros) if v is not None]
                if valores:
                    return valores[-1]                         # ultimo monto de la linea
        return None
