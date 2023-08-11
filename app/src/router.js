// router.js
import { createRouter, createWebHistory } from 'vue-router';
import Map from './components/Map.vue';
import Store from './components/Store.vue';
import BottomSheet from './components/BottomSheet.vue';

const routes = [
    { path: '/', component: Map },
    { path: '/store/:title', name: 'store', component: Store, props: true }
];
  

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
