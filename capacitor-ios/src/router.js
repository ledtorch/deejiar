import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: '/',
    name: 'launch',
    component: () => import('./components/common/LaunchScreen.vue')
  },
  {
    path: "/map",
    component: () => import("./components/Map.vue")
  },
  {
    path: "/detail/:id",
    name: "detail",
    component: () => import("./components/Detail.vue")
  },
  {
    path: "/account",
    name: "account",
    component: () => import("./views/Account.vue")
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to track page views
router.afterEach((to) => {
  // Use window.trackPageView function defined in index.html
  if (typeof window.trackPageView === 'function') {
    // Sends the full path of the current page to GA
    window.trackPageView(to.fullPath);
  }
});

export default router;
