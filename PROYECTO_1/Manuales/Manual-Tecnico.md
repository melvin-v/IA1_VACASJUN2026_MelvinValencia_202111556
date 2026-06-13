# Manual Técnico - Doctor Byte

Sistema experto para el diagnóstico de fallas comunes en computadoras.
Curso: Inteligencia Artificial 1 - Universidad de San Carlos de Guatemala.

---

## 1. Descripción general

Doctor Byte es un sistema experto basado en reglas. El usuario selecciona los
síntomas que presenta su equipo y el sistema infiere las posibles fallas y sus
recomendaciones. La inferencia se realiza en SWI-Prolog; una API REST en
FastAPI expone el motor; una interfaz web permite la interacción; cada
diagnóstico se notifica por Telegram y se guarda en un historial local.

El backend implementa una variante del patrón MVC adaptada a APIs REST,
conocida como Controller -> Service -> Repository:

```
Request HTTP
    |
    v
Controller        (define endpoints, valida tipos, delega al Service)
    |
    v
Service           (lógica de negocio, validaciones, arma respuestas)
    |
    v
Repository        (única capa que toca la fuente de datos)
    |
    v
SWI-Prolog / JSON / Telegram API
```

Hay tres repositorios distintos, uno por fuente de datos:

- `PrologRepository`: ejecuta el motor de inferencia en SWI-Prolog.
- `HistorialRepository`: persiste y lee el historial en un archivo JSON local.
- `TelegramNotifier`: envía las notificaciones a la API de Telegram.

---

## 2. Tecnologías utilizadas

| Componente            | Tecnología                          |
|-----------------------|-------------------------------------|
| Motor de inferencia   | SWI-Prolog 9                        |
| Backend / API         | Python 3.10+, FastAPI               |
| Servidor de aplicación| Uvicorn                             |
| Puente Python-Prolog  | PySwip                              |
| Cliente HTTP          | httpx                               |
| Variables de entorno  | python-dotenv                       |
| Interfaz web          | Vue 3 (vía CDN), HTML, CSS          |
| Notificaciones        | Telegram Bot API                    |
| Persistencia historial| Archivo JSON local                  |
| Contenedores          | Docker, Docker Compose              |
| Control de versiones  | Git, GitHub                         |

---

## 3. Estructura del proyecto

```
proyecto/
|- backend/
|  |- main.py                      Punto de entrada de FastAPI
|  |- requirements.txt             Dependencias de Python
|  |- .env.example                 Plantilla de variables de entorno
|  |- .gitignore
|  |- obtener_chat_id.py           Utilidad para obtener el chat_id de Telegram
|  |- probar_telegram.py           Utilidad para probar la conexión a Telegram
|  |- prolog/
|  |  \- doctor_byte.pl            Base de conocimiento (motor de inferencia)
|  |- data/
|  |  \- historial.json            Historial de diagnósticos (se crea solo)
|  \- app/
|     |- config.py                 Lectura de variables de entorno (.env)
|     |- schemas/
|     |  |- diagnostico_schema.py  Modelos Pydantic de entrada/salida
|     |  \- historial_schema.py    Modelo del registro de historial
|     |- repositories/
|     |  |- prolog_repository.py   Acceso a SWI-Prolog (PySwip)
|     |  \- historial_repository.py Acceso al JSON del historial
|     |- services/
|     |  \- diagnostico_service.py Lógica de negocio
|     |- controllers/
|     |  |- diagnostico_controller.py  Endpoints REST
|     |  \- dependencias.py        Inyección de dependencias
|     \- notifiers/
|        \- telegram_notifier.py   Servicio de notificación por Telegram
\- frontend/
   \- index.html                   Interfaz web (Vue por CDN, un solo archivo)
```

---

## 4. Base de conocimiento (Prolog)

El archivo `prolog/doctor_byte.pl` contiene el conocimiento del sistema experto.

### 4.1 Hechos

| Predicado            | Forma                       | Cantidad |
|----------------------|-----------------------------|----------|
| `sintoma/2`          | `sintoma(Id, Descripcion)`  | 20       |
| `falla/2`            | `falla(Id, Descripcion)`    | 12       |
| `recomendacion/2`    | `recomendacion(IdFalla, Texto)` | 12   |

### 4.2 Reglas de inferencia

`diagnostico/1` agrupa las 12 reglas. Una falla se diagnostica cuando están
presentes los síntomas que la caracterizan. Ejemplo:

```prolog
diagnostico(falla_fuente_poder) :-
    sintoma_activo(no_enciende),
    sintoma_activo(sin_energia).
```

### 4.3 Motor de inferencia

Los síntomas reportados se almacenan en el hecho dinámico `sintoma_activo/1`,
que se reescribe en cada consulta. Predicados principales:

- `cargar_sintomas(+Lista)`: limpia los síntomas previos y registra los nuevos.
- `registrar_sintomas(+Lista)`: recorre la lista con recursión y un corte (`!`).
- `diagnosticar(+ListaSintomas, -Fallas)`: devuelve la lista de IDs de fallas.
- `diagnostico_completo(+ListaSintomas, -Resultado)`: devuelve fallas con
  descripción y recomendación.
- `listar_sintomas(-Lista)`: devuelve el catálogo completo de síntomas.

La base de conocimiento cumple los requisitos del enunciado: uso de hechos,
reglas, variables, listas y al menos un corte.

---

## 5. Capa Repository

### 5.1 PrologRepository

Única capa que se comunica con SWI-Prolog a través de PySwip. Carga el archivo
`doctor_byte.pl` al iniciar y traduce entre tipos de Python y términos de
Prolog. Como la base usa hechos dinámicos globales, el acceso se serializa con
un lock para evitar que peticiones concurrentes se interfieran.

Métodos: `listar_sintomas()`, `diagnosticar(sintomas)`, `obtener_falla(id)`.

### 5.2 HistorialRepository

Única capa que toca el archivo JSON del historial. Lee y escribe registros, y
también usa un lock por la escritura concurrente. Si el archivo no existe o
está dañado, devuelve una lista vacía sin fallar.

Métodos: `guardar(registro)`, `listar(limite)`.

---

## 6. Capa Service

`DiagnosticoService` contiene la lógica de negocio. En el flujo de diagnóstico:

1. Valida que la lista de síntomas no esté vacía (de lo contrario, error 400).
2. Elimina duplicados conservando el orden.
3. Valida que cada síntoma exista en el catálogo (error 400 si alguno no
   existe). Esta validación también blinda contra inyección en Prolog, ya que
   solo átomos conocidos llegan al Repository.
4. Consulta el motor de inferencia y arma la lista de fallas.
5. Construye el mensaje de respuesta.
6. Guarda el diagnóstico en el historial.
7. Dispara la notificación por Telegram.

El método `listar_historial(limite)` devuelve los registros guardados.

---

## 7. Capa Controller y API REST

`diagnostico_controller.py` define los endpoints y delega toda la lógica al
Service. La inyección de dependencias se concentra en `dependencias.py`.

| Método | Ruta            | Descripción                                       |
|--------|-----------------|---------------------------------------------------|
| GET    | `/`             | Estado del servicio.                              |
| GET    | `/sintomas`     | Catálogo de síntomas disponibles.                 |
| POST   | `/diagnostico`  | Recibe síntomas y devuelve fallas y recomendaciones. |
| GET    | `/historial`    | Diagnósticos realizados, más reciente primero. Acepta `?limite=N`. |

### 7.1 Ejemplo: POST /diagnostico

Petición:

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

La documentación interactiva (Swagger UI) se genera automáticamente en `/docs`.

---

## 8. Notificaciones por Telegram

`TelegramNotifier` envía el diagnóstico al chat configurado usando el método
`sendMessage` de la Bot API. El envío se realiza en un hilo en segundo plano
para no bloquear la respuesta de la API; si Telegram falla o no está
configurado, el diagnóstico se entrega igual al usuario.

Requiere dos variables de entorno (ver sección 10): `TELEGRAM_BOT_TOKEN` y
`TELEGRAM_CHAT_ID`. Si no están definidas, la notificación simplemente se omite.

---

## 9. Persistencia del historial

Cada diagnóstico se guarda en `data/historial.json`. Cada registro contiene:

| Campo                | Descripción                              |
|----------------------|------------------------------------------|
| `id`                 | Identificador único del registro.        |
| `fecha`              | Fecha y hora local en formato ISO 8601.  |
| `sintomas_evaluados` | Síntomas que se enviaron.                |
| `fallas`             | Fallas detectadas con su recomendación.  |
| `mensaje`            | Mensaje resumen del diagnóstico.         |

La carpeta `data/` está en `.gitignore`: el historial es información de
ejecución y no se versiona en el repositorio.

---

## 10. Configuración

Las credenciales se manejan con variables de entorno, fuera del código.

1. Copiar `.env.example` como `.env`.
2. Completar las variables:

```
TELEGRAM_BOT_TOKEN=token_que_entrega_BotFather
TELEGRAM_CHAT_ID=id_del_chat_destino
```

El archivo `.env` contiene secretos y está en `.gitignore`; al repositorio
solo se sube `.env.example`.

Para obtener el `chat_id`: crear el bot con @BotFather, enviarle un mensaje y
ejecutar `python obtener_chat_id.py`. Para verificar la conexión:
`python probar_telegram.py`.

---

## 11. Instalación y ejecución

### 11.1 Requisitos previos

- Python 3.10 o superior.
- SWI-Prolog instalado en el sistema (lo requiere PySwip).
- Docker y Docker Compose (para la ejecución en contenedores).

### 11.2 Opción A: Docker Compose (recomendada)

El proyecto se ejecuta en contenedores con Docker Compose. Desde la raíz del
proyecto:

```bash
docker compose up --build
```

Esto construye y levanta los servicios definidos en `docker-compose.yml`. Una
vez arriba:

- API backend: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs
- Interfaz web: según el puerto del servicio de frontend definido en el compose.

Para detener los servicios:

```bash
docker compose down
```

Nota: los nombres de servicio y los puertos dependen del `docker-compose.yml`
del proyecto; ajustar estas indicaciones a esa configuración.

### 11.3 Opción B: ejecución local (sin Docker)

Backend:

```bash
cd backend
python -m venv venv
# Windows:   venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend (servir el archivo estático para evitar bloqueos de fetch):

```bash
cd frontend
python -m http.server 5500
```

Luego abrir http://localhost:5500. Si el backend corre en una dirección
distinta de http://localhost:8000, ajustar la constante `apiBase` al inicio del
script en `index.html`.

---

## 12. Flujo completo de una petición

1. El usuario selecciona síntomas en la interfaz web y presiona Diagnosticar.
2. El frontend envía `POST /diagnostico` con la lista de síntomas.
3. El Controller valida el tipo de dato y delega al Service.
4. El Service valida los síntomas y llama al PrologRepository.
5. El PrologRepository ejecuta la inferencia en SWI-Prolog y devuelve las fallas.
6. El Service arma la respuesta, la guarda en el historial y dispara la
   notificación de Telegram.
7. El frontend muestra el informe y refresca el panel de historial.

---

## 13. Consideraciones de diseño

- Concurrencia: el motor de Prolog usa estado global mutable y el historial es
  un archivo compartido; ambos accesos se protegen con locks.
- CORS: el backend habilita CORS para que la interfaz web pueda consumir la API
  desde el navegador.
- Tolerancia a fallos: la notificación de Telegram nunca interrumpe el
  diagnóstico; los errores se registran y se continúa.
- Separación de responsabilidades: cada capa tiene una única razón de cambio,
  lo que facilita las pruebas y el mantenimiento.