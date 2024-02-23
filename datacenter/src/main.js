import { createApp } from 'vue'
import { createPinia } from 'pinia'

// Components
import App from './App.vue'

// Plugin
import router from './router'

// Global CSS and normalize CSS
import 'normalize.css';
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
