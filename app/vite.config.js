import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import fs from 'fs';
// HTTPS Dependency


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],

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





  
