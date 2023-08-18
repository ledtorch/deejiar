// router.js
import { createRouter, createWebHistory } from 'vue-router';
import Map from './components/Map.vue';
import Store from './components/Store.vue';
import Account from './components/Account.vue';

const routes = [
    { path: '/', component: Map , meta: { title: 'BistroMap' }},
    { path: '/store/:title', name: 'store', component: Store, props: true },
    { path: '/account', component: Account, meta: { title: 'Account' }}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
