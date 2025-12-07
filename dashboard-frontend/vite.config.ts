import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // Vite domyślnie używa 5173
    proxy: {
      '/api': {
        // Domyślnie proxy do portu 8001 (oryginalny projekt)
        // Dla nowego projektu (8002) zmień na: 'http://localhost:8002'
        target: process.env.VITE_API_URL || 'http://localhost:8001',
        changeOrigin: true,
      }
    }
  }
})

