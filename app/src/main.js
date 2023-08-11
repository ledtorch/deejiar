import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js'

import './style.css'
// Global CSS

createApp(App).use(router).mount('#app')
