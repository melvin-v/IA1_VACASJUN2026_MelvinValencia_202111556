<script setup>
import { reactive, ref, onMounted } from 'vue'
import { api } from './api.js'
import MazeGrid from './components/MazeGrid.vue'
import Toolbar from './components/Toolbar.vue'
import MetricsPanel from './components/MetricsPanel.vue'

// ----------------------------- Estado ----------------------------- //
const mazes = ref([])              // catálogo de laberintos predefinidos
const selectedMazeId = ref('')
const workingMaze = ref(null)      // copia editable del laberinto actual
const mode = ref('wall')

const exploredSet = reactive(new Set()) // claves "r,c" exploradas (animación)
const pathSet = reactive(new Set())     // claves "r,c" de la ruta final

const lastResult = ref(null)
const comparison = ref([])
const error = ref('')
const busy = ref(false)
const connected = ref(true)

const sleep = (ms) => new Promise((res) => setTimeout(res, ms))
const cloneMaze = (m) => JSON.parse(JSON.stringify(m))

// --------------------------- Carga inicial ------------------------- //
onMounted(async () => {
  try {
    await api.health()
    mazes.value = await api.listMazes()
    if (mazes.value.length) {
      await selectMaze(mazes.value[0].id)
    }
  } catch (e) {
    connected.value = false
    error.value =
      'No se pudo conectar con la API. ¿Está el backend en ejecución?'
  }
})

// --------------------------- Acciones ------------------------------ //
async function selectMaze(id) {
  try {
    const maze = await api.getMaze(id)
    selectedMazeId.value = id
    workingMaze.value = cloneMaze(maze)
    clearOverlays()
  } catch (e) {
    error.value = e.message
  }
}

async function resetMaze() {
  if (selectedMazeId.value) await selectMaze(selectedMazeId.value)
}

function clearOverlays() {
  exploredSet.clear()
  pathSet.clear()
  lastResult.value = null
  comparison.value = []
  error.value = ''
}

function paint({ r, c }) {
  const m = workingMaze.value
  if (!m) return
  // Editar el laberinto invalida los resultados previos.
  if (exploredSet.size || pathSet.size) {
    exploredSet.clear()
    pathSet.clear()
    lastResult.value = null
    comparison.value = []
  }
  const isStart = m.start[0] === r && m.start[1] === c
  const isGoal = m.goal[0] === r && m.goal[1] === c

  switch (mode.value) {
    case 'wall':
      if (!isStart && !isGoal) m.grid[r][c] = 1
      break
    case 'erase':
      m.grid[r][c] = 0
      break
    case 'start':
      if (!isGoal) {
        m.grid[r][c] = 0
        m.start = [r, c]
      }
      break
    case 'goal':
      if (!isStart) {
        m.grid[r][c] = 0
        m.goal = [r, c]
      }
      break
  }
}

async function run(algorithm) {
  if (!workingMaze.value || busy.value) return
  error.value = ''
  comparison.value = []
  exploredSet.clear()
  pathSet.clear()
  busy.value = true
  try {
    const result = await api.search(workingMaze.value, algorithm)
    await animate(result)
    lastResult.value = result
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}

async function animate(result) {
  // 1) Animar el orden de exploración de nodos.
  const stepDelay = result.visited_order.length > 120 ? 4 : 12
  for (const [r, c] of result.visited_order) {
    exploredSet.add(`${r},${c}`)
    await sleep(stepDelay)
  }
  // 2) Trazar la ruta final paso a paso (si existe).
  for (const [r, c] of result.path) {
    pathSet.add(`${r},${c}`)
    await sleep(28)
  }
}

async function compare() {
  if (!workingMaze.value || busy.value) return
  error.value = ''
  exploredSet.clear()
  pathSet.clear()
  lastResult.value = null
  busy.value = true
  try {
    const res = await api.compare(workingMaze.value)
    comparison.value = res.results
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="layout">
    <header class="masthead">
      <div class="brand">
        <span class="logo">◣◢</span>
        <div>
          <h1>RoboMaze</h1>
          <p class="sub">Centro de Control · Búsqueda en Espacios de Estados</p>
        </div>
      </div>
      <div class="status">
        <span :class="['led', connected ? 'on' : 'off']"></span>
        {{ connected ? 'API conectada' : 'API desconectada' }}
      </div>
    </header>

    <Toolbar
      :mazes="mazes"
      :selected-maze-id="selectedMazeId"
      :mode="mode"
      :busy="busy"
      @select-maze="selectMaze"
      @set-mode="(m) => (mode = m)"
      @run="run"
      @compare="compare"
      @clear-overlays="clearOverlays"
      @reset-maze="resetMaze"
    />

    <main class="workspace">
      <section class="grid-area">
        <MazeGrid
          v-if="workingMaze"
          :maze="workingMaze"
          :explored-set="exploredSet"
          :path-set="pathSet"
          :editable="!busy"
          @paint="paint"
        />
        <p v-else class="loading">Cargando laberintos…</p>
      </section>

      <MetricsPanel
        :last-result="lastResult"
        :comparison="comparison"
        :error="error"
      />
    </main>

    <footer class="foot">
      Práctica 4 · Inteligencia Artificial 1 · Ingeniería en Ciencias y Sistemas · USAC
    </footer>
  </div>
</template>

<style scoped>
.layout {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.masthead {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
  padding-bottom: 1rem;
}

.brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  font-size: 2rem;
  color: var(--amber);
  text-shadow: var(--glow-amber);
}

h1 {
  font-size: 1.8rem;
  letter-spacing: 0.08em;
}

.sub {
  color: var(--text-dim);
  font-size: 0.78rem;
  letter-spacing: 0.05em;
}

.status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  color: var(--text-dim);
}

.led {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}
.led.on {
  background: var(--green);
  box-shadow: 0 0 8px var(--green);
  animation: pulse 2s infinite;
}
.led.off {
  background: var(--red);
  box-shadow: 0 0 8px var(--red);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.workspace {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 1.25rem;
  align-items: start;
}

.loading {
  color: var(--text-dim);
  padding: 3rem;
  text-align: center;
}

.foot {
  text-align: center;
  color: var(--text-dim);
  font-size: 0.72rem;
  letter-spacing: 0.06em;
  border-top: 1px solid var(--border);
  padding-top: 1rem;
}

@media (max-width: 900px) {
  .workspace {
    grid-template-columns: 1fr;
  }
}
</style>
