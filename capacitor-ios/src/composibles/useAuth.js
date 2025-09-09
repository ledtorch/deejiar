// src/composables/useAuth.js
import { computed, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/userStore';

export function useAuth() {
  const router = useRouter();
  const userStore = useUserStore();

  // Auth state
  const isAuthenticated = computed(() => userStore.isAuthenticated);
  const user = computed(() => userStore.user);
  const isLoading = computed(() => userStore.isLoading);
  const userState = computed(() => userStore.userState);

  // Check if route requires auth
  const requiresAuth = (route) => {
    return route.meta?.requiresAuth === true;
  };

  // Guard for protected routes
  const checkAuthGuard = (to) => {
    if (requiresAuth(to) && !isAuthenticated.value) {
      // Store intended destination
      sessionStorage.setItem('redirectAfterLogin', to.fullPath);
      return { name: 'login' };
    }
    return true;
  };

  // Redirect after successful login
  const handlePostLoginRedirect = () => {
    const redirectPath = sessionStorage.getItem('redirectAfterLogin');
    if (redirectPath) {
      sessionStorage.removeItem('redirectAfterLogin');
      router.push(redirectPath);
    } else {
      router.push({ name: 'home' });
    }
  };

  // Auto-refresh token when needed
  const setupTokenRefresh = () => {
    // Check token every 5 minutes
    const interval = setInterval(async () => {
      if (userStore.isAuthenticated) {
        const lastRefresh = userStore.lastTokenRefresh;
        const now = Date.now();
        const thirtyMinutes = 30 * 60 * 1000;

        if (!lastRefresh || (now - lastRefresh) > thirtyMinutes) {
          await userStore.refreshAccessToken();
        }
      }
    }, 5 * 60 * 1000); // 5 minutes

    // Clean up on component unmount
    return () => clearInterval(interval);
  };

  // Watch for auth changes
  watch(isAuthenticated, (newValue, oldValue) => {
    if (!oldValue && newValue) {
      // User just logged in
      console.log('User authenticated:', user.value);
      handlePostLoginRedirect();
    } else if (oldValue && !newValue) {
      // User just logged out
      console.log('User logged out');

      // If on protected route, redirect to home
      const currentRoute = router.currentRoute.value;
      if (requiresAuth(currentRoute)) {
        router.push({ name: 'home' });
      }
    }
  });

  return {
    // State
    isAuthenticated,
    user,
    isLoading,
    userState,

    // Methods
    checkAuthGuard,
    handlePostLoginRedirect,
    setupTokenRefresh,
    requiresAuth,

    // Store methods
    login: userStore.login,
    logout: userStore.logout,
    register: userStore.register,
    refreshToken: userStore.refreshAccessToken
  };
}