import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import dotenv from 'dotenv';

// CSS dependency
import autoprefixer from 'autoprefixer';

// HTTPS dependency
import fs from 'fs';

export default defineConfig({
  plugins: [
    vue(),
  ],
  css: {
    preprocessorOptions: {
      scss: {
      },
    },
    postcss: {
      plugins: [
        autoprefixer
      ],
    },
  },

  // Local https server
  server: {
    https: {
      key: fs.readFileSync('./localhost.key'),
      cert: fs.readFileSync('./localhost.crt'),
    },
  },

})