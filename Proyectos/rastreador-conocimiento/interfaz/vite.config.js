import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  build: {
    // FastAPI servirá los estáticos desde servidor/estaticos/
    outDir: path.resolve(__dirname, '../servidor/estaticos'),
    emptyOutDir: true,
  },
})
