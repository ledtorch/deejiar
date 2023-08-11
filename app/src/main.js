import { createApp } from 'vue'
import App from './App.vue'
import Map from "./components/Map.vue";
import Store from "./components/Store.vue";

import router from './router.js'


import './style.css'
// Global CSS


// const routes = [
//     { path: "/", component: Map },
//     { path: "/store/:title", name: "store", component: Store, props: true }
//   ];
  
//   const router = createRouter({
//     history: createWebHistory(),
//     routes
//   });
  
//   createApp(App)
//     .use(router)
//     .mount("#app");



createApp(App).use(router).mount('#app')
