import { createApp } from 'vue'
import { createHead } from '@vueuse/head'

// Components
import App from './App.vue'
import Map from "./components/Map.vue";
import Detail from "./components/Detail.vue";

// Plugin
import router from './router.js'
// import { createPinia } from 'pinia';

// Global CSS
import './style.css'

// Dependency
import 'mapbox-gl/dist/mapbox-gl.css';

const head = createHead()
const app = createApp(App)

app.use(router)
app.use(head)
app.mount('#app')
