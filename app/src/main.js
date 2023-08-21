import { createApp } from 'vue'
import App from './App.vue'
import Map from "./components/Map.vue";
import Detail from "./components/Detail.vue";

import router from './router.js'

import './style.css'
// Global CSS
import 'mapbox-gl/dist/mapbox-gl.css';
// Dependency

createApp(App).use(router).mount('#app')
