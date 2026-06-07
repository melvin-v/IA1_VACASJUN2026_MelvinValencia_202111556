# Manual de Usuario — Sistema de Rutas Guatemala

**Inteligencia Artificial 1 · Practica 1 · USAC FIUSAC**

---

## Tabla de contenidos

1. [Requisitos previos](#1-requisitos-previos)
2. [Instalacion](#2-instalacion)
3. [Como usar la aplicacion](#3-como-usar-la-aplicacion)
   - [Buscar la ruta mas corta](#31-buscar-la-ruta-mas-corta)
   - [Ver todas las rutas posibles](#32-ver-todas-las-rutas-posibles)
   - [Administrar ciudades y conexiones](#33-administrar-ciudades-y-conexiones)
4. [Ciudades disponibles](#4-ciudades-disponibles)
5. [Preguntas frecuentes](#5-preguntas-frecuentes)

---

## 1. Requisitos previos

Para correr el sistema necesitas tener instalado **una sola herramienta**:

| Herramienta | Version minima | Descarga |
|-------------|---------------|---------|
| Docker Desktop | 24.0 o superior | https://www.docker.com/products/docker-desktop |

> Docker incluye tanto Docker Engine como Docker Compose. No necesitas instalar Python, SWI-Prolog ni Nginx por separado — todo viene dentro de los contenedores.

---

## 2. Instalacion

### Paso 1 — Descargar el proyecto

Clona el repositorio o descarga el ZIP y descomprimelo:

```bash
git clone https://github.com/TU_USUARIO/[IA1]_VACASJUN2026_TU_NOMBRE_TU_CARNET.git
cd [IA1]_VACASJUN2026_TU_NOMBRE_TU_CARNET
```

### Paso 2 — Levantar el sistema

Desde la raiz del proyecto (donde esta `docker-compose.yml`), ejecuta:

```bash
docker compose up --build
```

La primera vez descarga las imagenes base (~500 MB). Las siguientes veces es inmediato.

Cuando veas esta linea en la consola, el sistema esta listo:

```
rutas_backend   | INFO:     Application startup complete.
```

### Paso 3 — Abrir en el navegador

Abre tu navegador y ve a:

```
http://localhost
```

Para detener el sistema:

```bash
docker compose down
```

---

## 3. Como usar la aplicacion

La aplicacion tiene tres secciones accesibles desde la barra de navegacion superior.

---

### 3.1 Buscar la ruta mas corta

Esta es la funcion principal. Encuentra el camino optimo (menor distancia total) entre dos departamentos.

**Pasos:**

1. Haz clic en **"Ruta corta"** en la barra de navegacion.
2. Selecciona el **Origen** en el primer desplegable (ej. `Guatemala`).
3. Selecciona el **Destino** en el segundo desplegable (ej. `Huehuetenango`).
4. Haz clic en **"Buscar ruta mas corta"**.

**Resultado:**

El sistema mostrara una tarjeta verde con:

- El camino completo representado como chips conectados con flechas:
  `Guatemala → Sacatepequez → Chimaltenango → Solola → Totonicapan → Huehuetenango`
- La distancia total en kilometros (ej. `244 km`)
- El numero de paradas
- Las estadisticas rapidas: km totales, paradas y tiempo aproximado de viaje

**Ejemplo de resultado:**

```
Ruta optima encontrada
Guatemala → Sacatepequez → Chimaltenango → Solola → Totonicapan → Huehuetenango
                                                                    244 km
5 paradas · Ruta mas eficiente entre Guatemala y Huehuetenango
```

**Errores comunes:**

| Mensaje | Causa | Solucion |
|---------|-------|----------|
| "El origen y el destino no pueden ser la misma ciudad" | Se selecciono el mismo departamento en ambos campos | Selecciona dos departamentos distintos |
| "No existe ninguna ruta entre X e Y" | No hay camino posible en el grafo actual | Agrega conexiones intermedias desde la seccion Administrar |

---

### 3.2 Ver todas las rutas posibles

Muestra **todas** las rutas existentes entre dos departamentos, ordenadas de menor a mayor distancia.

**Pasos:**

1. Haz clic en **"Todas las rutas"** en la navegacion.
2. Selecciona origen y destino.
3. Haz clic en **"Ver todas las rutas"**.

**Resultado:**

Una tabla con todas las rutas encontradas:

| # | Camino | Distancia |
|---|--------|-----------|
| 1 | Guatemala → Escuintla → Suchitepequez → Retalhuleu | 162 km |
| 2 | Guatemala → Sacatepequez → Escuintla → Retalhuleu | 185 km |
| 3 | ... | ... |

> Para rutas con muchos caminos posibles (ej. Guatemala → Retalhuleu tiene mas de 700), la tabla se pagina de 15 en 15. Usa los botones **"Anterior"** y **"Siguiente"** para navegar.

---

### 3.3 Administrar ciudades y conexiones

Permite expandir la base de conocimiento sin modificar codigo.

#### Agregar una nueva ciudad

1. Haz clic en **"Administrar"** en la navegacion.
2. En el campo **"Nombre del departamento"**, escribe el nombre (ej. `peten`).
3. Haz clic en **"+ Agregar ciudad"**.
4. Aparecera un mensaje verde confirmando que la ciudad fue agregada.

> El nombre se convierte automaticamente a minusculas. Puedes escribirlo con o sin tildes.

> **Nota importante:** Las ciudades agregadas desde la interfaz son temporales. Al reiniciar el sistema con `docker compose down` y `docker compose up` se pierden. Para hacerlas permanentes, agrega el hecho `ciudad(nombre).` directamente en `prolog/rutas.pl`.

#### Agregar una nueva conexion

1. Selecciona **Ciudad A** y **Ciudad B** en los desplegables.
2. Escribe la distancia en kilometros entre ambas.
3. Haz clic en **"+ Agregar conexion"**.

> Ambas ciudades deben existir en la base de conocimiento antes de poder conectarlas.

---

## 4. Ciudades disponibles

El sistema incluye 14 departamentos de Guatemala con sus distancias reales:

| Departamento | Conectado con |
|-------------|--------------|
| Guatemala | Escuintla, Sacatepequez, Chimaltenango, El Progreso, Baja Verapaz |
| Escuintla | Guatemala, Sacatepequez, Suchitepequez, Retalhuleu |
| Sacatepequez | Guatemala, Chimaltenango, Escuintla |
| Chimaltenango | Guatemala, Sacatepequez, Solola, Quiche, Baja Verapaz |
| Quetzaltenango | Solola, Totonicapan, Huehuetenango, Retalhuleu, Suchitepequez |
| Suchitepequez | Escuintla, Solola, Quetzaltenango, Retalhuleu |
| Retalhuleu | Escuintla, Quetzaltenango, Suchitepequez |
| Solola | Chimaltenango, Quetzaltenango, Totonicapan, Suchitepequez |
| Totonicapan | Solola, Quetzaltenango, Huehuetenango, Quiche |
| Huehuetenango | Quetzaltenango, Totonicapan, Quiche |
| Quiche | Chimaltenango, Totonicapan, Huehuetenango, Alta Verapaz, Baja Verapaz |
| Alta Verapaz | Quiche, Baja Verapaz |
| Baja Verapaz | Guatemala, Chimaltenango, Quiche, Alta Verapaz, El Progreso |
| El Progreso | Guatemala, Baja Verapaz |

---

## 5. Preguntas frecuentes

**¿Por que tarda la primera busqueda?**
La primera vez que se hace una consulta, Prolog carga toda la base de conocimiento en memoria. Las consultas siguientes son instantaneas.

**¿Las rutas son rutas reales de Guatemala?**
Si. Las distancias estan basadas en las carreteras principales entre departamentos.

**¿Puedo usar el sistema sin Docker?**
Si. Ver la seccion de desarrollo local en el Manual Tecnico (`MANUAL_TECNICO.md`).

**¿Por que hay cientos de rutas entre dos ciudades?**
Prolog encuentra todos los caminos posibles evitando repetir ciudades. Entre departamentos muy conectados (como Guatemala y Retalhuleu) existen mas de 700 combinaciones validas. La ruta mas corta siempre aparece primera en la tabla.

**¿Que pasa si el sistema no carga?**
Verifica que Docker Desktop este corriendo. Luego ejecuta:

```bash
docker compose logs backend
```

Si ves errores de Prolog, asegurate de que `prolog/rutas.pl` exista y no tenga errores de sintaxis.