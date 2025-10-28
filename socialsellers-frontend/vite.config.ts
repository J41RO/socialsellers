/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // Test config comentado para build de producción
  // Solo se usa en desarrollo con vitest
  // test: {
  //   globals: true,
  //   environment: 'jsdom',
  //   setupFiles: './src/tests/setup.ts',
  //   exclude: ['node_modules', 'e2e/**'],
  // },
})
