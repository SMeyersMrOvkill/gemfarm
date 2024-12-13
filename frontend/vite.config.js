import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/socket.io': {
        target: 'http://localhost:5000',
        ws: true
      },
      '/api': {
        target: 'http://localhost:5000'
      }
    }
  },
  build: {
    outDir: '../src/static/dist',
    assetsDir: '',
    emptyOutDir: true
  }
})
