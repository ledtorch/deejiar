import { createApp } from 'vue'
import App from './App.vue'

// Plugin
import router from './router.js'

// Global CSS and Tailwind
import './assets/tailwind.css';
import './style.css'

createApp(App).use(router).mount('#app')