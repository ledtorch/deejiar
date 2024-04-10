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

export default router;
