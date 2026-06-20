"""Sistema externo SIMULADO.

Expone un formulario web publico que el RPA (Playwright) llenara
automaticamente para 'registrar' la factura, tal como pide la practica.
"""
from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.simulated_record import SimulatedRecord
from app.repositories.simulated_record import SimulatedRecordRepository

router = APIRouter(prefix="/simulado", tags=["sistema-simulado"])

_FORM = """
<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Sistema Externo - Registro de Facturas</title>
<style>body{font-family:system-ui;max-width:520px;margin:40px auto;padding:0 16px}
input{display:block;width:100%;padding:8px;margin:6px 0 14px;box-sizing:border-box}
button{padding:10px 18px}</style></head>
<body><h2>Sistema Externo - Registro de Facturas</h2>
<form method="post" action="/simulado/registro">
<label>Numero de factura</label><input name="invoice_number" id="invoice_number">
<label>Fecha</label><input name="invoice_date" id="invoice_date">
<label>Proveedor</label><input name="provider_name" id="provider_name">
<label>NIT</label><input name="nit" id="nit">
<label>Total</label><input name="total" id="total">
<button type="submit" id="enviar">Registrar</button>
</form></body></html>
"""


@router.get("/form", response_class=HTMLResponse)
def form():
    return _FORM


@router.post("/registro", response_class=HTMLResponse)
def registro(
    invoice_number: str = Form(""),
    invoice_date: str = Form(""),
    provider_name: str = Form(""),
    nit: str = Form(""),
    total: str = Form(""),
    db: Session = Depends(get_db),
):
    SimulatedRecordRepository(db).add(SimulatedRecord(
        invoice_number=invoice_number, invoice_date=invoice_date,
        provider_name=provider_name, nit=nit, total=total, source="RPA",
    ))
    return '<html><body><h2 id="resultado">Registro exitoso</h2></body></html>'
