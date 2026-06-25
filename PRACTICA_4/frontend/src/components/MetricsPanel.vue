<script setup>
defineProps({
  lastResult: { type: Object, default: null },
  comparison: { type: Array, default: () => [] }, // lista de SearchResult
  error: { type: String, default: '' },
  legend: { type: Boolean, default: true },
})

function fmt(ms) {
  return `${ms.toFixed(3)} ms`
}
</script>

<template>
  <aside class="panel">
    <h2>// Telemetría</h2>

    <p v-if="error" class="error">⚠ {{ error }}</p>

    <!-- Resultado de una corrida individual -->
    <div v-if="lastResult" class="result-card">
      <div class="result-head">
        <span class="algo">{{ lastResult.algorithm }}</span>
        <span :class="['badge', lastResult.found ? 'ok' : 'fail']">
          {{ lastResult.found ? 'RUTA ENCONTRADA' : 'SIN RUTA' }}
        </span>
      </div>
      <dl class="metrics">
        <div><dt>Longitud de ruta</dt><dd>{{ lastResult.path_length }} pasos</dd></div>
        <div><dt>Nodos explorados</dt><dd>{{ lastResult.nodes_explored }}</dd></div>
        <div><dt>Tiempo</dt><dd>{{ fmt(lastResult.execution_time_ms) }}</dd></div>
      </dl>
    </div>

    <!-- Tabla comparativa BFS vs DFS -->
    <div v-if="comparison.length" class="compare">
      <h3>Comparación</h3>
      <table>
        <thead>
          <tr>
            <th>Algoritmo</th>
            <th>Ruta</th>
            <th>Pasos</th>
            <th>Nodos</th>
            <th>Tiempo</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in comparison" :key="r.algorithm">
            <td class="algo">{{ r.algorithm }}</td>
            <td>
              <span :class="['dot', r.found ? 'ok' : 'fail']"></span>
              {{ r.found ? 'Sí' : 'No' }}
            </td>
            <td>{{ r.path_length }}</td>
            <td>{{ r.nodes_explored }}</td>
            <td>{{ fmt(r.execution_time_ms) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="!lastResult && !comparison.length && !error" class="empty">
      Configura el laberinto y ejecuta un algoritmo para ver las métricas.
    </div>

    <!-- Leyenda de colores -->
    <div v-if="legend" class="legend">
      <h3>Leyenda</h3>
      <ul>
        <li><span class="sw start"></span> Inicio (A)</li>
        <li><span class="sw goal"></span> Meta (B)</li>
        <li><span class="sw wall"></span> Muro</li>
        <li><span class="sw explored"></span> Nodo explorado</li>
        <li><span class="sw path"></span> Ruta final</li>
      </ul>
    </div>
  </aside>
</template>

<style scoped>
.panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

h2 {
  font-size: 1rem;
  color: var(--cyan);
}
h3 {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-dim);
  margin-bottom: 0.6rem;
}

.error {
  color: var(--red);
  border: 1px solid rgba(255, 93, 93, 0.4);
  background: rgba(255, 93, 93, 0.08);
  padding: 0.6rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
}

.result-card {
  border: 1px solid var(--border-bright);
  border-radius: 6px;
  padding: 0.9rem;
  background: var(--panel-2);
}

.result-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.algo {
  font-family: var(--font-display);
  font-weight: 700;
  color: var(--amber);
  letter-spacing: 0.05em;
}

.badge {
  font-size: 0.65rem;
  font-family: var(--font-display);
  padding: 0.2rem 0.5rem;
  border-radius: 3px;
  letter-spacing: 0.08em;
}
.badge.ok {
  background: rgba(90, 209, 122, 0.15);
  color: var(--green);
  border: 1px solid rgba(90, 209, 122, 0.4);
}
.badge.fail {
  background: rgba(255, 93, 93, 0.12);
  color: var(--red);
  border: 1px solid rgba(255, 93, 93, 0.4);
}

.metrics {
  display: grid;
  gap: 0.5rem;
}
.metrics > div {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px dotted var(--border);
  padding-bottom: 0.35rem;
}
dt {
  color: var(--text-dim);
  font-size: 0.8rem;
}
dd {
  color: var(--text-bright);
  font-weight: 500;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8rem;
}
th,
td {
  text-align: left;
  padding: 0.45rem 0.4rem;
  border-bottom: 1px solid var(--border);
}
th {
  font-family: var(--font-display);
  color: var(--text-dim);
  font-size: 0.7rem;
  text-transform: uppercase;
}

.dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 4px;
}
.dot.ok {
  background: var(--green);
}
.dot.fail {
  background: var(--red);
}

.empty {
  color: var(--text-dim);
  font-size: 0.85rem;
  font-style: italic;
}

.legend ul {
  list-style: none;
  display: grid;
  gap: 0.45rem;
}
.legend li {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.8rem;
}
.sw {
  width: 16px;
  height: 16px;
  border-radius: 3px;
  flex-shrink: 0;
}
.sw.start {
  background: var(--green);
}
.sw.goal {
  background: var(--magenta);
}
.sw.wall {
  background: var(--wall);
}
.sw.explored {
  background: rgba(56, 217, 196, 0.5);
}
.sw.path {
  background: var(--amber);
}
</style>
