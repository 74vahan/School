import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// API calls go to the backend under /api during dev; in prod, the edge
// nginx (infra/nginx/nginx.conf) does this same /api -> app:8000 routing.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
