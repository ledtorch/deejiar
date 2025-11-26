import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { Purchases } from '@revenuecat/purchases-capacitor'

const API_ENDPOINT = import.meta.env.VITE_API_URL;

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref(null);
  const accessToken = ref(null);
  const refreshToken = ref(null);
  const isLoading = ref(false);
  const lastTokenRefresh = ref(null);

  // 🔒 Refresh lock to prevent race conditions (critical for iOS)
  let refreshPromise = null;

  // Auth
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value);
  const isNewUser = computed(() => user.value?.is_new_user || false);

  // Basic info
  const userUID = computed(() => user.value?.uid || '');
  const userEmail = computed(() => user.value?.email || '');
  const displayName = computed(() => user.value?.display_name || user.value?.email?.split('@')[0] || 'User');
  const avatarUrl = computed(() => user.value?.avatar_url || null);
  const userRegisteredAt = computed(() => user.value?.created_at || null);

  // Social accounts info
  const xAccount = computed(() => user.value?.['x-account'] || null);
  const xConnectedDate = computed(() => user.value?.['x-connected'] || null);
  const instagramAccount = computed(() => user.value?.['ig-account'] || null);
  const instagramConnectedDate = computed(() => user.value?.['ig-connected'] || null);

  // Subscription info
  const isPremium = computed(() => user.value?.premium || false);
  const subscriptionPlan = computed(() => user.value?.subscription_plan || null);
  const subscriptionStatus = computed(() => user.value?.subscription_status || null);
  const subscriptionStartedAt = computed(() => user.value?.subscription_started_at || null);
  const subscriptionExpiresAt = computed(() => user.value?.subscription_expires_at || null);

  // Subscription helper
  const isSubscriptionActive = computed(() => subscriptionStatus.value === 'active');
  const isSubscriptionTrial = computed(() => subscriptionStatus.value === 'trial');
  const isSubscriptionExpired = computed(() => subscriptionStatus.value === 'expired');
  const isSubscriptionCancelled = computed(() => subscriptionStatus.value === 'cancelled');

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
  const formattedRegistrationDate = computed(() => formatRegistrationDate(userRegisteredAt.value));

  // Actions
  const setAuth = (authData) => {
    if (!authData) return;

    // ✅ CRITICAL: Update in-memory state FIRST (before localStorage)
    // This ensures the token is immediately available even if localStorage write is delayed (iOS issue)
    accessToken.value = authData.access_token;
    refreshToken.value = authData.refresh_token;
    user.value = authData.user;
    lastTokenRefresh.value = Date.now();

    // Then persist to localStorage
    // Note: On iOS, these writes might be slightly delayed, but in-memory state is already correct
    try {
      localStorage.setItem('access_token', authData.access_token);
      localStorage.setItem('refresh_token', authData.refresh_token);
      localStorage.setItem('user', JSON.stringify(authData.user));
      localStorage.setItem('last_token_refresh', lastTokenRefresh.value);
    } catch (error) {
      console.error('Failed to persist auth data:', error);
    }

    scheduleTokenRefresh();
  };

  const clearAuth = () => {
    user.value = null;
    accessToken.value = null;
    refreshToken.value = null;
    lastTokenRefresh.value = null;
    refreshPromise = null; // Clear refresh lock

    // Clear localStorage
    try {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      localStorage.removeItem('last_token_refresh');
    } catch (error) {
      console.error('Failed to clear auth data:', error);
    }
  };

  const loadAuthFromStorage = async () => {
    try {
      const storedToken = localStorage.getItem('access_token');
      const storedRefreshToken = localStorage.getItem('refresh_token');
      const storedUser = localStorage.getItem('user');
      const storedLastRefresh = localStorage.getItem('last_token_refresh');

      if (storedToken && storedUser && storedRefreshToken) {
        // Load tokens into memory
        accessToken.value = storedToken;
        refreshToken.value = storedRefreshToken;

        // Check token age
        const lastRefresh = storedLastRefresh ? parseInt(storedLastRefresh) : 0;
        const tokenAge = Date.now() - lastRefresh;
        const fiftyMinutes = 50 * 60 * 1000;  // Supabase tokens expire in ~60 min

        if (tokenAge > fiftyMinutes) {
          // ✅ Token is likely expired - refresh FIRST before using
          console.log('🔄 Token may be expired, refreshing first...');
          const refreshed = await refreshAccessToken();
          if (!refreshed) {
            clearAuth();
            return;
          }
        }

        // If token is valid, load user from cache
        user.value = JSON.parse(storedUser);
        fetchCurrentUser();
      }
    } catch (error) {
      console.error('Failed to load auth from storage:', error);
      clearAuth();
    }
  }

  const refreshAccessToken = async () => {
    // 🔒 CRITICAL: If refresh is already in progress, return that promise
    // This prevents multiple simultaneous refresh attempts (common on iOS when app returns from background)
    if (refreshPromise) {
      return refreshPromise;
    }

    if (!refreshToken.value) {
      clearAuth();
      return false;
    }

    // 🔒 Create refresh promise with lock
    refreshPromise = (async () => {
      try {
        isLoading.value = true;

        // ✅ CRITICAL: Capture the current refresh token BEFORE making the request
        // This prevents the token from changing mid-request (iOS race condition fix)
        const currentRefreshToken = refreshToken.value;

        const response = await fetch(`${API_ENDPOINT}/user/auth/refresh`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh_token: currentRefreshToken })
        });

        if (response.ok) {
          const data = await response.json();
          setAuth(data);
          return true;
        } else if (response.status === 401) {
          // Refresh token expired, user needs to login again
          clearAuth();
          return false;
        } else {
          // Unexpected error
          clearAuth();
          return false;
        }
      } catch (error) {
        console.error('Token refresh failed:', error);
        clearAuth();
        return false;
      } finally {
        isLoading.value = false;
        // 🔒 Release lock
        refreshPromise = null;
      }
    })();

    return refreshPromise;
  };

  const fetchCurrentUser = async () => {
    if (!accessToken.value) return null;

    try {
      isLoading.value = true;

      const response = await fetch(`${API_ENDPOINT}/user/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${accessToken.value}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const userData = await response.json();

        console.log('[fetchCurrentUser] Fresh data from API:', {
          email: userData.email,
          premium: userData.premium,
          subscription_status: userData.subscription_status
        });

        user.value = userData;
        lastTokenRefresh.value = Date.now();

        localStorage.setItem('user', JSON.stringify(userData));
        localStorage.setItem('last_token_refresh', lastTokenRefresh.value);

        return userData;
      } else if (response.status === 401) {
        // Token expired, attempt refresh
        const refreshed = await refreshAccessToken();
        if (refreshed) {
          // Retry after successful refresh
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

    try {
      const uid = userUID.value;
      if (uid) {
        const res = await Purchases.logIn({ appUserID: uid });
        // res.created === true when RC created a new customer for this uid
        // res.customerInfo holds current entitlements
      }
    } catch (e) {
      console.warn('[RC] logIn failed', e);
    }

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
        await fetch(`${API_ENDPOINT}/user/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken.value}`,
            'Content-Type': 'application/json'
          }
        });
      }
      try {
        // Return to anonymous in RC
        await Purchases.logOut();
      } catch (e) {
        console.warn('[RC] logOut failed', e);
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

  // 🗝️ User state for TheAvatar component
  const userState = computed(() => {
    if (!isAuthenticated.value) return 'default';
    if (isPremium.value) return 'premium';
    return 'active';
  });

  const scheduleTokenRefresh = () => {
    setTimeout(() => {
      if (isAuthenticated.value) {
        refreshAccessToken();
      }
    }, 50 * 60 * 1000); // 50 minutes
  };


  return {
    // State
    user,
    accessToken,
    isLoading,

    // Auth
    isAuthenticated,
    isNewUser,

    // Basic info
    userUID,
    userEmail,
    displayName,
    avatarUrl,
    userRegisteredAt,

    // Social account info
    xAccount,
    xConnectedDate,
    instagramAccount,
    instagramConnectedDate,
    formattedXConnectedDate,
    formattedInstagramConnectedDate,
    formattedRegistrationDate,

    // Subscription info
    isPremium,
    subscriptionPlan,
    subscriptionStatus,
    subscriptionStartedAt,
    subscriptionExpiresAt,

    // Subscription helper
    isSubscriptionActive,
    isSubscriptionTrial,
    isSubscriptionExpired,
    isSubscriptionCancelled,

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

    // 🗝️
    userState
  };
});