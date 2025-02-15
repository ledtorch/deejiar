import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import dotenv from 'dotenv'
import path from 'path'

// HTTPS dependency
import fs from 'fs'

export default defineConfig({
  plugins: [vue()],

  // Local https server
  server: {
    https: {
      key: fs.readFileSync('./localhost.key'),
      cert: fs.readFileSync('./localhost.crt'),
    },
  },

  // The path redirection 
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  }
})