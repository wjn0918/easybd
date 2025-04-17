import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/easybd/',
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@c': fileURLToPath(new URL('./src/components', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5001/api',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/static':{
        target: 'http://127.0.0.1:5001/static',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/static/, '')
      }

    }
  }
})


