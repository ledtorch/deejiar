import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { fileURLToPath, URL } from 'node:url';

// HTTPS dependency
import fs from 'fs'

export default defineConfig({
  plugins: [vue()],

  server: {
    port: 5173,
    https: {
      key: fs.readFileSync('./localhost.key'),
      cert: fs.readFileSync('./localhost.crt'),
    },
  },

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  base: '/admin/',
});
