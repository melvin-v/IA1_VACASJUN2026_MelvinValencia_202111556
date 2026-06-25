# Manual de Usuario — RoboMaze

**Práctica 4 · Inteligencia Artificial 1 · Ingeniería en Ciencias y Sistemas · USAC**

---

## 1. ¿Qué es RoboMaze?

RoboMaze es una aplicación web que te permite construir laberintos y observar
cómo dos algoritmos de inteligencia artificial —**BFS** y **DFS**— encuentran un
camino desde un punto de inicio hasta una meta. Además de mostrar la ruta,
muestra cuántas casillas exploró cada algoritmo y cuánto tardó, para que puedas
compararlos.

## 2. Requisitos previos

- **Opción A (recomendada):** [Docker](https://www.docker.com/) y Docker Compose.
- **Opción B (desarrollo):** Python 3.11+ y Node.js 20+.

## 3. Instalación y ejecución

### 3.1 Con Docker Compose (un solo comando)

Desde la carpeta raíz del proyecto:

```bash
docker compose up --build
```

Cuando termine, abre en tu navegador:

- **Interfaz web:** <http://localhost:8080>
- **Documentación de la API (Swagger):** <http://localhost:8000/docs>

Para detener el sistema, presiona `Ctrl + C` y luego:

```bash
docker compose down
```

### 3.2 En modo desarrollo (sin Docker)

**Backend** (terminal 1):
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend** (terminal 2):
```bash
cd frontend
npm install
npm run dev
```

Luego abre <http://localhost:5173>.

## 4. Uso de la interfaz

La pantalla se divide en tres zonas: la **barra de herramientas** (arriba), el
**laberinto** (centro) y el panel de **telemetría** (derecha).

### 4.1 Elegir un laberinto

En la barra de herramientas, usa el menú **Laberinto** para escoger uno de los 5
laberintos predefinidos. Uno de ellos (*Sin Salida*) está diseñado a propósito
para que **no exista** una ruta válida, y así probar el manejo de errores.

### 4.2 Editar el laberinto

El selector **Edición** define qué hace el clic sobre la cuadrícula:

| Modo     | Acción                                                       |
|----------|--------------------------------------------------------------|
| **Muro** | Coloca obstáculos. Puedes mantener presionado y arrastrar.   |
| **Borrar** | Elimina obstáculos (vuelve la casilla transitable).        |
| **Inicio** | Mueve el punto de partida (A).                             |
| **Meta**   | Mueve el destino (B).                                      |

### 4.3 Ejecutar un algoritmo

En **Acciones**:

- **▶ BFS** ejecuta Breadth-First Search y anima la exploración.
- **▶ DFS** ejecuta Depth-First Search y anima la exploración.
- **Comparar** ejecuta ambos y muestra una tabla comparativa.
- **Limpiar** borra la animación actual sin perder el laberinto.
- **Restaurar** vuelve el laberinto a su estado predefinido original.

Mientras corre la animación, las casillas exploradas se iluminan en cian y, al
final, la ruta encontrada se resalta en ámbar.

### 4.4 Leer las métricas

En el panel de telemetría verás, para la última ejecución:

- **Longitud de ruta:** número de pasos del origen al destino.
- **Nodos explorados:** cuántas casillas examinó el algoritmo.
- **Tiempo:** duración de la búsqueda en milisegundos.

Al usar **Comparar**, la tabla muestra estas métricas lado a lado para BFS y DFS.

## 5. Interpretación de resultados

- **BFS** siempre encuentra la **ruta más corta** en número de pasos, pero suele
  explorar más casillas.
- **DFS** puede encontrar una ruta más larga, pero a veces explora menos casillas.
- Si la meta está encerrada por muros, ambos reportarán **"Sin ruta"**.

Esta diferencia es justamente el aprendizaje central de la práctica: comparar
estrategias de exploración y entender sus compromisos.

## 6. Evidencias de funcionamiento

> Inserta aquí las capturas de pantalla que demuestren el funcionamiento del
> sistema. Se recomienda incluir al menos las siguientes:

1. **Laberinto cargado** con inicio, meta y obstáculos.
   `![Laberinto inicial](img/01_laberinto.png)`
2. **Ejecución de BFS** con la ruta encontrada resaltada.
   `![BFS](img/02_bfs.png)`
3. **Ejecución de DFS** con su ruta.
   `![DFS](img/03_dfs.png)`
4. **Tabla comparativa** BFS vs DFS.
   `![Comparación](img/04_comparacion.png)`
5. **Caso sin ruta** mostrando el mensaje correspondiente.
   `![Sin ruta](img/05_sin_ruta.png)`

## 7. Solución de problemas

| Síntoma                                   | Causa probable / Solución                                  |
|-------------------------------------------|------------------------------------------------------------|
| "API desconectada" en la cabecera         | El backend no está corriendo. Verifica el contenedor o uvicorn. |
| El puerto 8080 u 8000 está ocupado        | Cambia el mapeo de puertos en `docker-compose.yml`.        |
| El frontend no carga estilos/fuentes      | Verifica conexión a internet (las fuentes vienen de Google Fonts). |
| `docker compose` no se reconoce           | Instala Docker Desktop o usa la versión `docker-compose`.  |
