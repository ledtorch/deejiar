import { createApp } from 'vue'
import App from './App.vue'
import Map from "./components/Map.vue";
import Detail from "./components/Detail.vue";

import router from './router.js'

// Global CSS
import './style.css'

// Dependency
import 'mapbox-gl/dist/mapbox-gl.css';

createApp(App).use(router).mount('#app')
