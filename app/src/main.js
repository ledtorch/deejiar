import { createApp } from 'vue'
import { createHead } from '@unhead/vue'

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
createApp(App).use(router).use(head).mount('#app')