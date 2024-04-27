import { createApp } from 'vue'
import App from './App.vue'

// Plugin
import router from './router.js'

// Global CSS and normalize CSS
import 'normalize.css';
import './style.css'

const head = createHead()
createApp(App).use(router).mount('#app')