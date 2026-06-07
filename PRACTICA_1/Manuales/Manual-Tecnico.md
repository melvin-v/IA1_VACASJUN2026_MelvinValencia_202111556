# Manual Tecnico — Sistema de Rutas Guatemala

**Inteligencia Artificial 1 · Practica 1 · USAC FIUSAC**

---

## Tabla de contenidos

1. [Arquitectura del sistema](#1-arquitectura-del-sistema)
2. [Patron de arquitectura: MVC por capas](#2-patron-de-arquitectura-mvc-por-capas)
3. [Estructura del proyecto](#3-estructura-del-proyecto)
4. [Componente Prolog](#4-componente-prolog)
5. [Componente Backend Python](#5-componente-backend-python)
6. [Componente Frontend Vue.js](#6-componente-frontend-vuejs)
7. [Infraestructura Docker](#7-infraestructura-docker)
8. [Flujo completo de una peticion](#8-flujo-completo-de-una-peticion)
9. [Integracion Python-Prolog via PySwip](#9-integracion-python-prolog-via-pyswip)
10. [Desarrollo local sin Docker](#10-desarrollo-local-sin-docker)
11. [Posibles mejoras futuras](#11-posibles-mejoras-futuras)

---

## 1. Arquitectura del sistema

El sistema implementa una arquitectura de tres capas completamente separadas:

```
[ Navegador ]
     |  HTTP :80
[ Nginx ]  ←── sirve index.html + hace proxy de /api/*
     |  HTTP interno
[ FastAPI + PySwip ]  ←── valida, orquesta, formatea
     |  llamada de libreria (in-process)
[ SWI-Prolog ]  ←── TODA la logica de busqueda de rutas
```

**Principio de diseno central:** Prolog es el motor de inteligencia. Python es exclusivamente una capa de integracion. Ningun algoritmo de busqueda o calculo de distancias existe en Python.

---

## 2. Patron de arquitectura: MVC por capas

El backend implementa una variante del patron **MVC** adaptada a APIs REST, conocida como **Controller → Service → Repository**:

```
Request HTTP
    ↓
Controller          (rutas_controller.py)
  - Define endpoints con @router.get / @router.post
  - Valida tipos de parametros via FastAPI
  - Delega toda logica al Service
    ↓
Service             (rutas_service.py)
  - Contiene logica de negocio
  - Valida que ciudades existan antes de consultar Prolog
  - Lanza HTTPException con mensajes claros al usuario
  - Formatea resultados del Repository en schemas Pydantic
    ↓
Repository          (prolog_repository.py)
  - UNICA capa que toca SWI-Prolog directamente
  - Usa PySwip para ejecutar consultas
  - Traduce entre tipos Python y terminos Prolog
    ↓
SWI-Prolog          (rutas.pl)
  - Responde con variables unificadas
```

**Por que este patron:**

| Beneficio | Ejemplo en este proyecto |
|-----------|-------------------------|
| Aislamiento de cambios | Actualizar PySwip 0.2 → 0.3 solo afecto `prolog_repository.py` |
| Testabilidad | Se puede probar el Service con un Repository falso (mock) |
| Claridad de responsabilidades | El Controller nunca sabe que existe Prolog |
| Cumple restricciones del enunciado | La logica vive en Prolog; Python solo orquesta |

---

## 3. Estructura del proyecto

```
proyecto_rutas/
├── docker-compose.yml          ← orquestacion de contenedores
│
├── prolog/
│   └── rutas.pl                ← base de conocimiento + reglas de busqueda
│
├── backend/
│   ├── Dockerfile              ← imagen Python 3.11 + SWI-Prolog (multi-stage)
│   ├── requirements.txt        ← fastapi, uvicorn, pyswip, pydantic
│   ├── main.py                 ← punto de entrada FastAPI, CORS, router
│   ├── controllers/
│   │   └── rutas_controller.py ← endpoints REST
│   ├── services/
│   │   └── rutas_service.py    ← logica de negocio
│   ├── repositories/
│   │   └── prolog_repository.py← puente Python ↔ Prolog
│   └── models/
│       └── schemas.py          ← modelos Pydantic (entrada y salida)
│
├── frontend/
│   ├── Dockerfile              ← imagen Nginx Alpine
│   ├── nginx.conf              ← proxy /api/ → backend:8000
│   └── index.html              ← SPA Vue 3 (sin build step)
│
└── docs/
    ├── MANUAL_USUARIO.md
    └── MANUAL_TECNICO.md       ← este archivo
```

---

## 4. Componente Prolog

**Archivo:** `prolog/rutas.pl`

### Predicados principales

| Predicado | Aridad | Tipo | Descripcion |
|-----------|--------|------|-------------|
| `ciudad/1` | 1 | Hecho | Declara un departamento |
| `conectado/3` | 3 | Hecho | `conectado(A, B, Km)` — conexion directa con distancia |
| `arista/3` | 3 | Regla | Hace bidireccionales las conexiones |
| `ruta/5` | 5 | Regla | Busca un camino con lista de visitados anti-ciclos |
| `todas_rutas/3` | 3 | Regla | Recopila todas las rutas via `findall/3` |
| `ruta_mas_corta/4` | 4 | Regla | Obtiene la ruta de menor distancia |
| `minima/2` | 2 | Regla | Auxiliar recursivo para encontrar el minimo |
| `ciudad_existe/1` | 1 | Regla | Valida existencia de una ciudad |
| `agregar_ciudad/1` | 1 | Regla | Inserta hecho via `assertz/1` (dinamico) |
| `agregar_conexion/3` | 3 | Regla | Inserta conexion via `assertz/1` (dinamico) |
| `listar_ciudades/1` | 1 | Regla | Devuelve lista via `findall/3` |

### Logica anti-ciclos

El predicado `ruta/5` recibe una lista `Visitados` que crece en cada llamada recursiva:

```prolog
ruta(Origen, Destino, Visitados, [Origen | Resto], DistTotal) :-
    arista(Origen, Siguiente, D1),
    Siguiente \= Destino,
    \+ member(Siguiente, Visitados),   % <-- evita ciclos
    ruta(Siguiente, Destino, [Siguiente | Visitados], Resto, D2),
    DistTotal is D1 + D2.
```

`\+ member(Siguiente, Visitados)` falla si `Siguiente` ya fue visitado, lo que hace que Prolog retroceda (backtrack) y pruebe otra arista. Esto garantiza que cada camino encontrado no repita ciudades.

### Predicados dinamicos

Los hechos `ciudad/1` y `conectado/3` se declaran con `:- dynamic` para permitir `assertz/1` en tiempo de ejecucion. Esto es lo que permite agregar ciudades y conexiones desde la interfaz sin reiniciar el servidor.

---

## 5. Componente Backend Python

### Endpoints de la API

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| `GET` | `/` | Healthcheck y listado de endpoints |
| `GET` | `/api/ciudades` | Lista todas las ciudades |
| `GET` | `/api/ruta/corta?origen=X&destino=Y` | Ruta mas corta entre X e Y |
| `GET` | `/api/ruta/todas?origen=X&destino=Y` | Todas las rutas entre X e Y |
| `POST` | `/api/ciudades` | Agrega nueva ciudad |
| `POST` | `/api/conexiones` | Agrega nueva conexion |

Documentacion interactiva (Swagger UI) disponible en: `http://localhost:8000/docs`

### Schemas Pydantic

**Entrada:**

```python
class NuevaCiudad(BaseModel):
    nombre: str   # se normaliza a minusculas con validador

class NuevaConexion(BaseModel):
    ciudad_a: str
    ciudad_b: str
    distancia_km: int   # debe ser > 0
```

**Salida:**

```python
class RutaResponse(BaseModel):
    camino: List[str]    # ["guatemala", "escuintla", "retalhuleu"]
    distancia_km: int
    num_paradas: int

class RutaMasCorta(BaseModel):
    origen: str
    destino: str
    ruta: RutaResponse
    mensaje: str
```

### Singleton del Repository

`PrologRepository` implementa el patron Singleton para garantizar que el archivo `.pl` se cargue una sola vez al iniciar el servidor:

```python
def __new__(cls) -> "PrologRepository":
    if cls._instance is None:
        cls._instance = super().__new__(cls)
        cls._instance._inicializar()   # consult() solo aqui
    return cls._instance
```

Cada request reutiliza la misma instancia de Prolog con la base de conocimiento ya cargada en memoria.

---

## 6. Componente Frontend Vue.js

**Archivo:** `frontend/index.html`

Vue 3 se carga via CDN (`unpkg.com/vue@3`) sin paso de compilacion. Esto simplifica el despliegue: el archivo HTML es completamente autocontenido.

### Estado reactivo por vista

```javascript
// Vista 1: ruta mas corta
const corta = ref({ origen: '', destino: '', resultado: null, error: '' })

// Vista 2: todas las rutas
const todas = ref({ origen: '', destino: '', resultado: null, error: '' })
const pagina = ref(1)

// Vista 3: admin
const admin = ref({ nuevaCiudad: '', conexion: {...}, ... })
```

### Paginacion con computed

```javascript
const rutasPaginadas = computed(() => {
    const inicio = (pagina.value - 1) * porPagina
    return todas.value.resultado.rutas.slice(inicio, inicio + porPagina)
})
```

`computed` recalcula automaticamente cuando `pagina` o `todas.resultado` cambian.

### Deteccion de entorno

```javascript
const API = window.location.port === '5500'
    ? 'http://localhost:8000/api'   // desarrollo local
    : '/api'                         // Docker (Nginx hace proxy)
```

---

## 7. Infraestructura Docker

### Dockerfile del backend (multi-stage)

```dockerfile
# Stage 1: obtener binarios de SWI-Prolog
FROM swipl:9.0.4 AS prolog-base

# Stage 2: imagen final liviana
FROM python:3.11-slim-bookworm
COPY --from=prolog-base /usr/lib/swi-prolog /usr/lib/swi-prolog
COPY --from=prolog-base /usr/bin/swipl       /usr/bin/swipl
```

El multi-stage build evita incluir las herramientas de compilacion de SWI-Prolog en la imagen final, reduciendo el tamano considerablemente.

### Volumen del archivo Prolog

```yaml
volumes:
  - ./prolog:/app/prolog:ro
```

El archivo `rutas.pl` se monta como volumen de solo lectura (`:ro`). Esto permite modificar la base de conocimiento sin reconstruir la imagen Docker. Solo se necesita reiniciar el contenedor del backend:

```bash
docker compose restart backend
```

### Red interna

```yaml
networks:
  rutas_net:
    driver: bridge
```

Los contenedores se comunican usando sus nombres de servicio como hostnames (`http://backend:8000`). El puerto 8000 del backend no necesita estar expuesto publicamente en produccion — solo Nginx (puerto 80) necesita ser accesible.

### Healthcheck y dependencias

```yaml
backend:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/"]
    interval: 10s
    retries: 5

frontend:
  depends_on:
    backend:
      condition: service_healthy
```

Nginx espera hasta que el backend responda exitosamente antes de arrancar. Esto evita errores 502 Bad Gateway durante el inicio.

---

## 8. Flujo completo de una peticion

Ejemplo: usuario busca ruta de Guatemala a Quetzaltenango.

```
1. Usuario hace clic en "Buscar ruta mas corta"

2. Vue.js ejecuta:
   fetch('/api/ruta/corta?origen=guatemala&destino=quetzaltenango')

3. Nginx recibe la peticion en :80
   → proxy_pass http://backend:8000/api/ruta/corta?...

4. FastAPI → rutas_controller.py
   ruta_mas_corta(origen="guatemala", destino="quetzaltenango")

5. Controller llama a RutasService.obtener_ruta_mas_corta()

6. Service valida:
   - origen != destino ✓
   - ciudad_existe("guatemala") → consulta Prolog → True ✓
   - ciudad_existe("quetzaltenango") → consulta Prolog → True ✓

7. Service llama a PrologRepository.obtener_ruta_mas_corta()

8. Repository ejecuta via PySwip:
   prolog.query("ruta_mas_corta(guatemala, quetzaltenango, Camino, Dist)")

9. SWI-Prolog:
   - Ejecuta todas_rutas(guatemala, quetzaltenango, Rutas)
   - Dentro: findall recopila todas las rutas via ruta/5 con backtracking
   - minima/2 encuentra la de menor Dist
   - Unifica: Camino = [guatemala, sacatepequez, chimaltenango, solola, quetzaltenango]
              Dist = 156

10. Repository traduce: camino = ["guatemala", ...], distancia = 156

11. Service construye RutaMasCorta(ruta=RutaResponse(...))

12. Controller retorna JSON:
    {
      "origen": "guatemala",
      "destino": "quetzaltenango",
      "ruta": {
        "camino": ["guatemala","sacatepequez","chimaltenango","solola","quetzaltenango"],
        "distancia_km": 156,
        "num_paradas": 5
      },
      "mensaje": "Ruta mas corta encontrada exitosamente."
    }

13. Vue.js recibe el JSON y actualiza corta.resultado
    → Vue re-renderiza automaticamente mostrando los chips y la distancia
```

---

## 9. Integracion Python-Prolog via PySwip

PySwip es un wrapper de Python sobre la libreria C de SWI-Prolog (`libswipl`). La comunicacion ocurre en el mismo proceso — no hay sockets ni HTTP entre Python y Prolog.

### Como funciona `prolog.query()`

```python
from pyswip import Prolog
p = Prolog()
p.consult("rutas.pl")

# query() devuelve un generador de soluciones
for sol in p.query("ruta_mas_corta(guatemala, escuintla, C, D)"):
    print(sol["C"])  # ['guatemala', 'escuintla']
    print(sol["D"])  # 58
```

Cada variable en mayuscula en la consulta Prolog (C, D) se convierte en una clave del diccionario `sol`.

### Diferencia entre PySwip 0.2.x y 0.3.x

PySwip 0.3.x (compatible con SWI-Prolog 9.x) cambio como serializa los terminos compuestos devueltos por `findall`. Los terminos de la forma `ruta([...], 156)` ahora llegan como strings en vez de objetos `Functor`. Por eso el metodo `obtener_todas_rutas` usa backtracking directo en vez de `findall`:

```python
# En vez de parsear el string "ruta(['guatemala',...], 156)"
# usamos el predicado ruta/5 directamente y dejamos que
# PySwip itere sobre todas las soluciones con backtracking
query = f"ruta({origen}, {destino}, [{origen}], Camino, Dist)"
resultados = list(self._prolog.query(query))
```

---

## 10. Desarrollo local sin Docker

Si prefieres correr el proyecto sin Docker durante el desarrollo:

### Requisitos

- Python 3.11+
- SWI-Prolog 9.x instalado en el sistema
- Un servidor HTTP simple para el frontend

### Pasos

```bash
# 1. Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 2. Frontend (en otra terminal)
cd frontend
python3 -m http.server 5500
# Abrir: http://localhost:5500

# La URL de la API se detecta automaticamente:
# puerto 5500 → llama a http://localhost:8000/api
```

### Instalar SWI-Prolog en cada sistema operativo

| Sistema | Comando |
|---------|---------|
| Ubuntu/Debian | `sudo apt install swi-prolog` |
| macOS | `brew install swi-prolog` |
| Windows | Descargar instalador desde https://www.swi-prolog.org/Download.html |

---

## 11. Posibles mejoras futuras

### Mejoras al motor Prolog

- **Heuristica A\*:** implementar busqueda informada con estimacion de distancia euclidiana entre coordenadas geograficas reales de los departamentos. Reduciria drasticamente el espacio de busqueda.
- **Pesos multiples:** agregar un segundo criterio de optimizacion (ej. tiempo de viaje considerando tipo de carretera) como un tercer argumento en `conectado/4`.
- **Persistencia:** guardar `assertz` en un archivo secundario `.pl` para que las ciudades agregadas dinamicamente sobrevivan reinicios.

### Mejoras al backend

- **Cache:** usar `functools.lru_cache` en el Service para cachear rutas frecuentes. La ruta Guatemala→Quetzaltenango se consultara miles de veces — calcularla una sola vez tiene sentido.
- **Tests automatizados:** agregar `pytest` con tests unitarios para cada capa (Repository con un `.pl` de prueba, Service con Repository mockeado, endpoints con `TestClient` de FastAPI).
- **Autenticacion:** agregar JWT si se despliega como API publica para controlar quien puede agregar ciudades.

### Mejoras al frontend

- **Mapa interactivo:** integrar Leaflet.js con coordenadas reales de los departamentos y dibujar la ruta encontrada sobre el mapa de Guatemala.
- **Comparador visual:** mostrar un grafico de barras con las 10 rutas mas cortas usando Chart.js.
- **Modo offline:** usar Service Workers para cachear las ciudades y mostrarlas aunque el backend no este disponible.

### Mejoras a la infraestructura

- **CI/CD:** agregar GitHub Actions que construya y pruebe los contenedores en cada push al repositorio.
- **Nginx HTTPS:** configurar certificado SSL con Let's Encrypt para despliegue en servidor publico.
- **Escalabilidad:** separar el proceso de SWI-Prolog en su propio contenedor con una API interna, permitiendo multiples instancias del backend Python.