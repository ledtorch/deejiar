import { createApp } from 'vue'
import App from './App.vue'

// Plugin
import router from './router.js'

// Global CSS and Tailwind
import './assets/tailwind.css'
import './style.css'

// Import VueLazyload plugin
import VueLazyload from 'vue-lazyload'

// Create the app instance
const app = createApp(App)

// Use plugins
app.use(router)
app.use(VueLazyload, {
  preLoad: 1.3,
  attempt: 1
})

// Mount the app
app.mount('#app')