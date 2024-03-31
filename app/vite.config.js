import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import dotenv from 'dotenv';
// import { visualizer } from 'rollup-plugin-visualizer';


// CSS Dependency
import autoprefixer from 'autoprefixer';

// HTTPS Dependency
import fs from 'fs';

export default defineConfig({
  plugins: [
    vue(),
    // visualizer({ open: true, filename: 'bundle-report.html' })
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

  // HTTPS Server
  server: {
    https: {
      key: fs.readFileSync('./localhost.key'),
      cert: fs.readFileSync('./localhost.crt'),
    },
  },

})