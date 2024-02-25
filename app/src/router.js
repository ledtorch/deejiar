import { createRouter, createWebHistory } from "vue-router";
import Map from "./components/Map.vue";
import Detail from "./components/Detail.vue";
import Account from "./components/Account.vue";

const routes = [
  { path: "/", component: Map },
  {
    path: "/detail/:title",
    name: "detail",
    component: Detail
  },
  {
    path: "/account",
    name: "Account",
    component: Account
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
