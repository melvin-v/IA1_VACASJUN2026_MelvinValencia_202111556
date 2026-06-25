<script setup>
defineProps({
  mazes: { type: Array, required: true },
  selectedMazeId: { type: String, default: '' },
  mode: { type: String, required: true },
  busy: { type: Boolean, default: false },
})

const emit = defineEmits([
  'select-maze',
  'set-mode',
  'run',
  'compare',
  'clear-overlays',
  'reset-maze',
])

const modes = [
  { id: 'wall', label: 'Muro' },
  { id: 'erase', label: 'Borrar' },
  { id: 'start', label: 'Inicio' },
  { id: 'goal', label: 'Meta' },
]
</script>

<template>
  <div class="toolbar">
    <div class="group">
      <label>Laberinto</label>
      <select
        :value="selectedMazeId"
        :disabled="busy"
        @change="emit('select-maze', $event.target.value)"
      >
        <option v-for="m in mazes" :key="m.id" :value="m.id">
          {{ m.name }}
        </option>
      </select>
    </div>

    <div class="group">
      <label>Edición</label>
      <div class="btn-row">
        <button
          v-for="m in modes"
          :key="m.id"
          :class="{ active: mode === m.id }"
          :disabled="busy"
          @click="emit('set-mode', m.id)"
        >
          {{ m.label }}
        </button>
      </div>
    </div>

    <div class="group">
      <label>Acciones</label>
      <div class="btn-row">
        <button class="primary" :disabled="busy" @click="emit('run', 'BFS')">
          ▶ BFS
        </button>
        <button class="primary" :disabled="busy" @click="emit('run', 'DFS')">
          ▶ DFS
        </button>
        <button :disabled="busy" @click="emit('compare')">Comparar</button>
        <button :disabled="busy" @click="emit('clear-overlays')">Limpiar</button>
        <button :disabled="busy" @click="emit('reset-maze')">Restaurar</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  padding: 1rem 1.25rem;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 8px;
}

.group {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

label {
  font-family: var(--font-display);
  font-size: 0.7rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-dim);
}

.btn-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}
</style>
