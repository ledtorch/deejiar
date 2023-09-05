import { createRouter, createWebHistory } from "vue-router";
import Map from "./components/Map.vue";
import Detail from "./components/Detail.vue";
import Account from "./components/Account.vue";

const routes = [
  { path: "/", component: Map, meta: { title: "ínlōopmap" } },
  {
    path: "/detail/:title",
    name: "detail",
    component: Detail,
    props: (route) => ({
      title: route.params.title,

      // Convert the string back to an object in Detail.vue
      dataFromBottomSheet: JSON.parse(route.params.dataFromBottomSheet),
    }),
    meta: { title: "Detail" },
  },
  { path: "/account", component: Account, meta: { title: "Account" } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
