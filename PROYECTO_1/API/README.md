# Doctor Byte - Backend (FastAPI)

API REST que expone el sistema experto de diagnostico de fallas. Implementa el
patron en capas **Controller -> Service -> Repository**, donde el Repository es
la unica capa que se comunica con SWI-Prolog (via PySwip).

## Arquitectura

```
Request HTTP
    v
Controller   (app/controllers/diagnostico_controller.py)
  - Define los endpoints REST
  - Valida tipos via FastAPI/Pydantic
  - Delega la logica al Service
    v
Service      (app/services/diagnostico_service.py)
  - Logica de negocio
  - Valida que los sintomas existan antes de consultar Prolog
  - Lanza HTTPException con mensajes claros
  - Arma los schemas Pydantic de respuesta
    v
Repository   (app/repositories/prolog_repository.py)
  - UNICA capa que toca SWI-Prolog (PySwip)
  - Traduce entre tipos Python y terminos Prolog
    v
SWI-Prolog   (prolog/doctor_byte.pl)
```

## Estructura

```
backend/
|- main.py                      # crea la app FastAPI e incluye el router
|- requirements.txt
|- prolog/
|  \- doctor_byte.pl            # base de conocimiento (Etapa 1)
\- app/
   |- schemas/diagnostico_schema.py    # modelos Pydantic
   |- repositories/prolog_repository.py
   |- services/diagnostico_service.py
   \- controllers/
      |- diagnostico_controller.py
      \- dependencias.py        # instancia unica de las capas
```

## Requisitos previos

1. **Python 3.10 o superior.**
2. **SWI-Prolog instalado en el sistema** (PySwip lo necesita).
   - Windows: descargar de https://www.swi-prolog.org/download/stable
   - Linux (Debian/Ubuntu): `sudo apt install swi-prolog`
   - macOS: `brew install swi-prolog`

## Instalacion

```bash
cd backend
python -m venv venv
# Windows:  venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

```bash
uvicorn main:app --reload
```

- API: http://localhost:8000
- Documentacion interactiva (Swagger): http://localhost:8000/docs

## Endpoints

| Metodo | Ruta           | Descripcion                                  |
|--------|----------------|----------------------------------------------|
| GET    | `/`            | Estado del servicio.                         |
| GET    | `/sintomas`    | Catalogo de sintomas disponibles.            |
| POST   | `/diagnostico` | Recibe sintomas y devuelve fallas + recomendaciones. |

### Ejemplo de POST /diagnostico

Peticion:
```json
{ "sintomas": ["no_enciende", "sin_energia"] }
```

Respuesta:
```json
{
  "sintomas_evaluados": ["no_enciende", "sin_energia"],
  "fallas": [
    {
      "id": "falla_fuente_poder",
      "descripcion": "Falla en la fuente de poder",
      "recomendacion": "Verifique el cable de poder y pruebe con otra fuente; si persiste, reemplace la fuente de poder."
    }
  ],
  "mensaje": "Se identificaron 1 posible(s) falla(s)."
}
```
