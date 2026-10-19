import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// Configuração padrão do Vite para React + Tailwind
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
})