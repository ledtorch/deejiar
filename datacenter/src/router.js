import { createRouter, createWebHistory } from 'vue-router'
import TheAdmin from '@/components/TheAdmin.vue'
import TheGenerator from '@/components/TheGenerator.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: TheAdmin
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: TheGenerator,
    meta: { requiresAuth: true }
  }
];

// Initialize base URL to align client-side routing with the application's subdirectory structure
const router = createRouter({
  history: createWebHistory('/admin/'),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!localStorage.getItem('access_token')) {
      next({
        path: '/',
        query: { redirect: to.fullPath }
      });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router
