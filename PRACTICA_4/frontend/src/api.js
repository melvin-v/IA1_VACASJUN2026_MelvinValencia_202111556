const BASE = '/api'

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    let detail = `Error ${res.status}`
    try {
      const body = await res.json()
      if (body.detail) detail = body.detail
    } catch (_) {
      /* respuesta sin cuerpo JSON */
    }
    throw new Error(detail)
  }
  return res.json()
}

export const api = {
  health: () => request('/health'),
  algorithms: () => request('/algorithms'),
  listMazes: () => request('/mazes'),
  getMaze: (id) => request(`/mazes/${id}`),
  search: (maze, algorithm) =>
    request('/search', {
      method: 'POST',
      body: JSON.stringify({ maze, algorithm }),
    }),
  compare: (maze, algorithms = null) =>
    request('/compare', {
      method: 'POST',
      body: JSON.stringify({ maze, algorithms }),
    }),
}
