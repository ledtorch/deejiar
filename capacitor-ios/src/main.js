import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';

// Global CSS and Tailwind
import './assets/tailwind.css'
import './style.css';

// Plugin
import router from './router.js'
import { useMapStore } from './stores/mapStore'
import { useUserStore } from './stores/userStore';
import VueLazyload from 'vue-lazyload'

// Create Pinia and app instance
const pinia = createPinia();
const app = createApp(App)

// Use plugins
app.use(pinia);
app.use(router);
app.use(VueLazyload, {
  preLoad: 1.3,
  attempt: 1
})

// Initialize auth before mounting
async function initializeApp() {
  const mapStore = useMapStore();
  const userStore = useUserStore();

  // Run both operations in parallel
  await Promise.all([
    mapStore.initialize(),
    userStore.loadAuthFromStorage()
  ]);

  app.mount('#app');
}

initializeApp();






