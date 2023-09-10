import { createApp } from 'vue'

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

// Initialize and use Pinia
// const pinia = createPinia();
// app.use(pinia);

createApp(App).use(router).mount('#app')
