import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// HTTPS dependency
import fs from 'fs'

export default defineConfig({
  plugins: [vue()],

  // Local https server
  server: {
    port: 5174,
    https: {
      key: fs.readFileSync('./certs/localhost.key'),
      cert: fs.readFileSync('./certs/localhost.crt'),
    },
  },

  // The path redirection 
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  }
})