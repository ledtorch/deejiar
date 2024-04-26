import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    component: () => import("./components/Map.vue")
  },
  {
    path: "/detail/:title",
    name: "detail",
    component: () => import("./components/Detail.vue")
  },
  {
    path: "/account",
    name: "Account",
    component: () => import("./components/Account.vue")
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
