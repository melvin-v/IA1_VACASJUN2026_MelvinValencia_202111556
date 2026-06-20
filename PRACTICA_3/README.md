# SmartInvoice

Sistema inteligente de procesamiento de facturas con **Computer Vision, OCR y RPA**.
Práctica 3 · Inteligencia Artificial 1 · Universidad San Carlos de Guatemala.

## Características
- Carga de facturas (PDF/JPG/JPEG/PNG) y extracción automática por **OCR + OpenCV** (local).
- Extrae número, fecha, proveedor, NIT, subtotal, impuestos y total; valida y asigna estado.
- **Autenticación JWT**, CRUD de proveedores, bitácora de procesamiento.
- **Reportes** administrativos en PDF, Excel y CSV; envío por correo (SMTP).
- **RPA** con Playwright que registra la factura en un sistema web simulado.
- **Panel web admin** (HTML/CSS/JS) y API REST documentada (Swagger).
- Arquitectura por capas con **repository pattern** (FastAPI + SQLAlchemy + Alembic).

## Arranque rápido
```bash
cp .env.example .env
docker compose up --build
```
- Panel admin: http://localhost:8000/app
- API (Swagger): http://localhost:8000/docs

## Uso
1. Entrá a `/app`, creá tu cuenta e ingresá.
2. (Opcional) registrá proveedores con su NIT.
3. Subí una factura en "Procesar factura": corre el OCR y muestra los datos extraídos.
4. Revisá "Facturas" (con filtro por estado), dispará el **RPA** por fila.
5. Consultá la "Bitácora" y descargá/enviá "Reportes".

## Stack
Python · FastAPI · SQLAlchemy 2.0 · Alembic · PostgreSQL · JWT · OpenCV · Tesseract ·
Playwright · ReportLab · OpenPyXL · Docker · Docker Compose.

## Documentación
- `docs/MANUAL_TECNICO.md` — arquitectura, módulos, API, BD, requerimientos funcionales.
- `docs/REQUERIMIENTOS_NO_FUNCIONALES.md`
- `docs/DESPLIEGUE.md` — despliegue local y en la nube.

## Estructura
```
app/ (core · models · repositories · schemas · services · api/routes · static)
alembic/  docs/  Dockerfile  docker-compose.yml  requirements.txt
```
