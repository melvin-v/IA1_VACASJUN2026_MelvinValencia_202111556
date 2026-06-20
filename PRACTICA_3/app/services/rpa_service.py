"""Automatizacion RPA con Playwright.

Abre el formulario del sistema simulado, llena los campos con los datos
de la factura y lo envia, verificando el mensaje de exito.
"""
from __future__ import annotations

from app.core.config import settings
from app.models.invoice import Invoice


class RPAService:
    def register_invoice(self, invoice: Invoice) -> str:
        # Import perezoso: solo se necesita Playwright al ejecutar el RPA.
        from playwright.sync_api import sync_playwright

        url = f"{settings.BASE_URL}/simulado/form"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=settings.RPA_HEADLESS)
            page = browser.new_page()
            page.goto(url, wait_until="load")
            page.fill("#invoice_number", invoice.invoice_number or "")
            page.fill("#invoice_date", invoice.invoice_date or "")
            page.fill("#provider_name", invoice.provider_name or "")
            page.fill("#nit", invoice.nit or "")
            page.fill("#total", str(invoice.total or ""))
            page.click("#enviar")
            page.wait_for_selector("#resultado", timeout=5000)
            mensaje = page.inner_text("#resultado")
            browser.close()
        return mensaje
