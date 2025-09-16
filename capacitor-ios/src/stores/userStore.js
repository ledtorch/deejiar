// src/stores/userStore.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

const API_ENDPOINT = import.meta.env.VITE_API_URL;

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref(null);
  const accessToken = ref(null);
  const refreshToken = ref(null);
  const isLoading = ref(false);
  const lastTokenRefresh = ref(null);

  // Computed
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value);
  const isNewUser = computed(() => user.value?.is_new_user || false);
  const isPremium = computed(() => user.value?.premium || false);
  const userEmail = computed(() => user.value?.email || '');
  const userUID = computed(() => user.value?.uid || '');
  const displayName = computed(() => user.value?.display_name || user.value?.email?.split('@')[0] || 'User');
  const avatarUrl = computed(() => user.value?.avatar_url || null);

  // New computed properties for social accounts
  const xAccount = computed(() => user.value?.['x-account'] || null);
  const instagramAccount = computed(() => user.value?.['ig-account'] || null);
  const xConnectedDate = computed(() => user.value?.['x-connected'] || null);
  const instagramConnectedDate = computed(() => user.value?.['ig-connected'] || null);
  const userCreatedAt = computed(() => user.value?.created_at || null);

  // Helper function to format dates
  const formatConnectedDate = (dateString) => {
    if (!dateString) return null;
    try {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `Connected on ${year}.${month}.${day}`;
    } catch (error) {
      return null;
    }
  };

  // Helper function to format registration date
  const formatRegistrationDate = (dateString) => {
    if (!dateString) return null;
    try {
      const date = new Date(dateString);
      const monthNames = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
      ];
      const month = monthNames[date.getMonth()];
      const day = date.getDate();
      const year = date.getFullYear();
      return `Joined ${month}. ${day}, ${year}`;
    } catch (error) {
      return null;
    }
  };

  // Formatted date computed properties
  const formattedXConnectedDate = computed(() => formatConnectedDate(xConnectedDate.value));
  const formattedInstagramConnectedDate = computed(() => formatConnectedDate(instagramConnectedDate.value));
  const formattedRegistrationDate = computed(() => formatRegistrationDate(userCreatedAt.value));

  // User state for TheAvatar component
  const userState = computed(() => {
    if (!isAuthenticated.value) return 'default';
    if (isPremium.value) return 'premium';
    return 'active';
  });

  // Actions
  const setAuth = (authData) => {
    if (!authData) return;

    accessToken.value = authData.access_token;
    refreshToken.value = authData.refresh_token;
    user.value = authData.user;
    lastTokenRefresh.value = Date.now();

    // Persist to localStorage
    localStorage.setItem('access_token', authData.access_token);
    localStorage.setItem('refresh_token', authData.refresh_token);
    localStorage.setItem('user', JSON.stringify(authData.user));
    localStorage.setItem('last_token_refresh', lastTokenRefresh.value);
  };

  const clearAuth = () => {
    user.value = null;
    accessToken.value = null;
    refreshToken.value = null;
    lastTokenRefresh.value = null;

    // Clear localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    localStorage.removeItem('last_token_refresh');
  };

  const loadAuthFromStorage = async () => {
    try {
      const storedToken = localStorage.getItem('access_token');
      const storedRefresh = localStorage.getItem('refresh_token');
      const storedUser = localStorage.getItem('user');
      const storedLastRefresh = localStorage.getItem('last_token_refresh');

      if (storedToken && storedUser) {
        accessToken.value = storedToken;
        refreshToken.value = storedRefresh;
        user.value = JSON.parse(storedUser);
        lastTokenRefresh.value = storedLastRefresh ? parseInt(storedLastRefresh) : null;

        // Check if token needs refresh (older than 30 minutes)
        const thirtyMinutes = 30 * 60 * 1000;
        const shouldRefresh = !lastTokenRefresh.value ||
          (Date.now() - lastTokenRefresh.value) > thirtyMinutes;

        if (shouldRefresh && storedRefresh) {
          await refreshAccessToken();
        } else {
          // Verify token is still valid by fetching user profile
          await fetchCurrentUser();
        }
      }
    } catch (error) {
      console.error('Failed to load auth from storage:', error);
      clearAuth();
    }
  };

  const refreshAccessToken = async () => {
    if (!refreshToken.value) {
      clearAuth();
      return false;
    }

    try {
      isLoading.value = true;

      const response = await fetch(`${API_ENDPOINT}/api/user/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken.value })
      });

      if (response.ok) {
        const data = await response.json();
        setAuth(data);
        return true;
      } else if (response.status === 401) {
        // Refresh token expired, user needs to login again
        clearAuth();
        return false;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
      clearAuth();
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  const fetchCurrentUser = async () => {
    if (!accessToken.value) return null;

    try {
      isLoading.value = true;

      const response = await fetch(`${API_ENDPOINT}/api/user/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${accessToken.value}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const userData = await response.json();
        user.value = userData;
        localStorage.setItem('user', JSON.stringify(userData));
        return userData;
      } else if (response.status === 401) {
        // Token expired, try to refresh
        const refreshed = await refreshAccessToken();
        if (refreshed) {
          // Retry with new token
          return fetchCurrentUser();
        }
      }
    } catch (error) {
      console.error('Failed to fetch user profile:', error);
    } finally {
      isLoading.value = false;
    }

    return null;
  };

  const login = async (authData) => {
    setAuth(authData);

    // Mark as not new user after successful login
    if (user.value && user.value.is_new_user) {
      user.value.is_new_user = false;
      localStorage.setItem('user', JSON.stringify(user.value));
    }

    return true;
  };

  const register = async (authData) => {
    setAuth(authData);

    // New users are automatically logged in
    return true;
  };

  const logout = async () => {
    try {
      if (accessToken.value) {
        // Notify backend about logout
        await fetch(`${API_ENDPOINT}/api/user/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken.value}`,
            'Content-Type': 'application/json'
          }
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      clearAuth();
    }
  };

  const updateUserProfile = (updates) => {
    if (!user.value) return;

    user.value = { ...user.value, ...updates };
    localStorage.setItem('user', JSON.stringify(user.value));
  };

  return {
    // State
    user,
    accessToken,
    isLoading,

    // Computed
    isAuthenticated,
    isNewUser,
    isPremium,
    userEmail,
    userUID,
    displayName,
    avatarUrl,
    userState,

    // New social account computed properties
    xAccount,
    instagramAccount,
    xConnectedDate,
    instagramConnectedDate,
    userCreatedAt,
    formattedXConnectedDate,
    formattedInstagramConnectedDate,
    formattedRegistrationDate,

    // Actions
    setAuth,
    clearAuth,
    loadAuthFromStorage,
    refreshAccessToken,
    fetchCurrentUser,
    login,
    register,
    logout,
    updateUserProfile,
    getDeviceId,
    linkAppleAccount
  };
});