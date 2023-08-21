import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import autoprefixer from 'autoprefixer';
// CSS Dependency

import fs from 'fs';
// HTTPS Dependency

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
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

  // // Normal Server
  // server: {
  //   host: '0.0.0.0'
  // }
  
  // HTTPS Server
  server: {
    https: {
      key: fs.readFileSync('./localhost.key'),
      cert: fs.readFileSync('./localhost.crt'),
    },
  },

})