import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// En desarrollo, las peticiones a /api se redirigen al backend (puerto 8000).
// En producción, nginx hace ese proxy (ver frontend/nginx.conf), por lo que
// el código del frontend siempre llama a rutas relativas /api/...
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
