// export default router;
import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import { Capacitor } from '@capacitor/core'

// Platform detection
const isIOS = Capacitor.getPlatform() === 'ios'

// Routes configuration
const routes = [
  {
    path: '/',
    component: () => isIOS
      ? import('./components/ios/Map.vue')
      : import('./components/web/Map.vue')
  },
  {
    path: '/detail/:title',
    name: "detail",
    component: () => isIOS
      ? import('./components/ios/Detail.vue')
      : import('./components/web/Detail.vue')
  },
  {
    path: '/account',
    name: "Account",
    component: () => isIOS
      ? import('./components/ios/Account.vue')
      : import('./components/web/Account.vue')
  },
]

// Use different history modes for iOS and web
const history = isIOS
  ? createWebHashHistory()
  : createWebHistory()

// Create router instance
const router = createRouter({
  history,
  routes
})

// Navigation guard to track page views
router.afterEach((to) => {
  if (typeof window.trackPageView === 'function') {
    window.trackPageView(to.fullPath);
  }
});

// 🏗️ Add iOS-specific guard
router.beforeEach((to, from, next) => {
  if (isIOS) {
    // iOS-specific navigation logic
    // For example, handling deep links or native transitions
  }
  next()
})

export default router