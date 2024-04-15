import { createApp } from 'vue'

// Components
import App from './App.vue'

// Plugin
import router from './router'

// Global CSS and Tailwind CSS
import './assets/tailwind.css';
import './style.css'

const app = createApp(App)

app.use(router)

app.mount('#app')
