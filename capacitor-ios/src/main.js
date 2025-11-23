import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';

// Global CSS and Tailwind
import './assets/tailwind.css'
import './style.css';

// Plugin
import router from './router.js'
import VueLazyload from 'vue-lazyload'
import { useMapStore } from './stores/mapStore'
import { useUserStore } from './stores/userStore';
import { Capacitor } from '@capacitor/core';
import { Purchases } from '@revenuecat/purchases-capacitor'

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

  console.log('🚀 Initializing app...');

  // 🔍 DEBUG: Check localStorage before loading
  console.log('📦 localStorage contents:', {
    hasAccessToken: !!localStorage.getItem('access_token'),
    hasRefreshToken: !!localStorage.getItem('refresh_token'),
    hasUser: !!localStorage.getItem('user'),
  });

  // 1) restore auth (once)
  await Promise.all([
    mapStore.initialize(),
    userStore.loadAuthFromStorage(),
  ])

  console.log("userStore.user: ", userStore.user)

  // 2) configure RC with your public key and the UID (or null for anon) on iOS platform
  if (Capacitor.isNativePlatform() && Capacitor.getPlatform() === 'ios') {
    await Purchases.configure({
      apiKey: import.meta.env.VITE_RC_PUBLIC_KEY_IOS,
      appUserID: userStore.userUID || null,
    })
  }

  app.mount('#app');
}

initializeApp();






