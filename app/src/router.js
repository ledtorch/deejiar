import { createRouter, createWebHistory } from "vue-router";
import Map from "./components/Map.vue";
import Detail from "./components/Detail.vue";
import Account from "./components/Account.vue";

const routes = [
  { path: "/", component: Map },
  {
    path: "/detail/:title",
    name: "detail",
    component: Detail,
    meta: { title: "Detail" },
  },
  { path: "/account", component: Account, meta: { title: "Account" } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
