import { createApp } from 'vue'
import { createHead } from '@unhead/vue'

// Vue
import App from './App.vue'

// Plugin
import router from './router.js'

// Global CSS and normalize CSS
import 'normalize.css';
import './style.css'

const head = createHead()
createApp(App).use(router).use(head).mount('#app')