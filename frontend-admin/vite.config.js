import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3001,
    proxy: {
      '/api/admin': {
        target: 'http://localhost:5001',
        changeOrigin: true
      },
      '/admin/images': {
        target: 'http://localhost:5001',
        changeOrigin: true
      }
    }
  }
})