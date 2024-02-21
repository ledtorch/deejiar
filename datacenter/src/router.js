import { createRouter, createWebHistory } from 'vue-router'
import TheAdm from '@/components/TheAdm.vue' // Adjust the path based on your file structure
import TheGenerator from '@/components/TheGenerator.vue' // Adjust the path based on your file structure

const routes = [
  {
    path: '/',
    name: 'Home',
    component: TheAdm
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: TheGenerator,
    meta: { requiresAuth: true } // Add this line
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  // Check if the route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!localStorage.getItem('access_token')) {
      // This route requires auth, redirect to login page.
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      });
    } else {
      next();
    }
  } else {
    next(); // Make sure to always call next()!
  }
});

export default router
