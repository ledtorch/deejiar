import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: '/',
    name: 'launch',
    component: () => import('./components/common/LaunchScreen.vue')
  },
  {
    path: "/map",
    component: () => import("./views/Map.vue")
  },
  {
    path: "/detail/:id",
    name: "detail",
    component: () => import("./views/Detail.vue")
  },
  {
    path: "/plaza",
    name: "plaza",
    component: () => import("./views/Plaza.vue")
  },
  {
    path: "/account",
    name: "account",
    component: () => import("./views/Account.vue")
  },
  {
    path: "/profile/:uid",
    name: "profile",
    component: () => import("./views/Profile.vue")
  },
  {
    path: "/subscription",
    name: "subscription",
    component: () => import("./views/Subscription.vue")
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
