<script setup>
import { computed } from 'vue'

const props = defineProps({
  maze: { type: Object, required: true },     // { grid, start, goal }
  exploredSet: { type: Object, required: true }, // Set de claves "r,c"
  pathSet: { type: Object, required: true },      // Set de claves "r,c"
  editable: { type: Boolean, default: true },
})

const emit = defineEmits(['paint'])

const rows = computed(() => props.maze.grid.length)
const cols = computed(() => props.maze.grid[0]?.length || 0)

let painting = false

function key(r, c) {
  return `${r},${c}`
}

function isStart(r, c) {
  return props.maze.start[0] === r && props.maze.start[1] === c
}
function isGoal(r, c) {
  return props.maze.goal[0] === r && props.maze.goal[1] === c
}

function cellClass(r, c) {
  const classes = ['cell']
  if (props.maze.grid[r][c] === 1) classes.push('wall')
  if (props.exploredSet.has(key(r, c))) classes.push('explored')
  if (props.pathSet.has(key(r, c))) classes.push('path')
  if (isStart(r, c)) classes.push('start')
  if (isGoal(r, c)) classes.push('goal')
  return classes
}

function onDown(r, c) {
  if (!props.editable) return
  painting = true
  emit('paint', { r, c })
}
function onEnter(r, c) {
  if (!props.editable || !painting) return
  emit('paint', { r, c })
}
function stopPaint() {
  painting = false
}
</script>

<template>
  <div class="grid-wrap" @mouseup="stopPaint" @mouseleave="stopPaint">
    <div
      class="grid"
      :style="{
        gridTemplateColumns: `repeat(${cols}, 1fr)`,
        gridTemplateRows: `repeat(${rows}, 1fr)`,
      }"
    >
      <template v-for="(row, r) in maze.grid" :key="r">
        <div
          v-for="(_, c) in row"
          :key="`${r}-${c}`"
          :class="cellClass(r, c)"
          @mousedown.prevent="onDown(r, c)"
          @mouseenter="onEnter(r, c)"
        >
          <span v-if="isStart(r, c)" class="marker">A</span>
          <span v-else-if="isGoal(r, c)" class="marker">B</span>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.grid-wrap {
  display: flex;
  justify-content: center;
  padding: 1.25rem;
  background: var(--bg-grid);
  border: 1px solid var(--border);
  border-radius: 8px;
  box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.5);
}

.grid {
  display: grid;
  gap: 2px;
  width: min(560px, 100%);
  aspect-ratio: 1 / 1;
  user-select: none;
}

.cell {
  background: #161f30;
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: background-color 0.12s ease, box-shadow 0.12s ease;
}

.cell:hover {
  outline: 1px solid var(--border-bright);
}

.cell.wall {
  background: var(--wall);
  background-image: repeating-linear-gradient(
    45deg,
    rgba(0, 0, 0, 0.25) 0,
    rgba(0, 0, 0, 0.25) 2px,
    transparent 2px,
    transparent 5px
  );
}

.cell.explored {
  background: rgba(56, 217, 196, 0.28);
  box-shadow: inset 0 0 6px rgba(56, 217, 196, 0.4);
  animation: pop 0.2s ease;
}

.cell.path {
  background: var(--amber);
  box-shadow: var(--glow-amber);
}

.cell.start {
  background: var(--green);
  box-shadow: 0 0 12px rgba(90, 209, 122, 0.6);
}

.cell.goal {
  background: var(--magenta);
  box-shadow: 0 0 12px rgba(232, 93, 156, 0.6);
}

.marker {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 0.8rem;
  color: #0a0e17;
}

@keyframes pop {
  from {
    transform: scale(0.6);
    opacity: 0.4;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
