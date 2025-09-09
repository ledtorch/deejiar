// src/utils/authInterceptor.js
import { useUserStore } from '../stores/userStore';

class AuthInterceptor {
  constructor() {
    this.baseURL = import.meta.env.VITE_API_URL;
    this.requestQueue = [];
    this.isRefreshing = false;
  }

  async request(url, options = {}) {
    const userStore = useUserStore();
    const fullUrl = url.startsWith('http') ? url : `${this.baseURL}${url}`;

    // Add auth header if authenticated
    if (userStore.isAuthenticated) {
      options.headers = {
        ...options.headers,
        'Authorization': `Bearer ${userStore.accessToken}`
      };
    }

    try {
      let response = await fetch(fullUrl, options);

      // Handle 401 - Token expired
      if (response.status === 401 && userStore.refreshToken) {
        if (!this.isRefreshing) {
          this.isRefreshing = true;

          // Try to refresh token
          const refreshed = await userStore.refreshAccessToken();
          this.isRefreshing = false;

          if (refreshed) {
            // Retry original request with new token
            options.headers['Authorization'] = `Bearer ${userStore.accessToken}`;
            response = await fetch(fullUrl, options);
          } else {
            // Refresh failed, redirect to login
            this.handleAuthFailure();
          }

          // Process queued requests
          this.processRequestQueue(refreshed);
        } else {
          // Wait for token refresh to complete
          await this.waitForTokenRefresh();

          // Retry with new token
          if (userStore.isAuthenticated) {
            options.headers['Authorization'] = `Bearer ${userStore.accessToken}`;
            response = await fetch(fullUrl, options);
          }
        }
      }

      return response;
    } catch (error) {
      console.error('Request failed:', error);
      throw error;
    }
  }

  async get(url, options = {}) {
    return this.request(url, { ...options, method: 'GET' });
  }

  async post(url, body, options = {}) {
    return this.request(url, {
      ...options,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      body: JSON.stringify(body)
    });
  }

  async put(url, body, options = {}) {
    return this.request(url, {
      ...options,
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      body: JSON.stringify(body)
    });
  }

  async delete(url, options = {}) {
    return this.request(url, { ...options, method: 'DELETE' });
  }

  waitForTokenRefresh() {
    return new Promise((resolve) => {
      this.requestQueue.push(resolve);
    });
  }

  processRequestQueue(success) {
    this.requestQueue.forEach(resolve => resolve(success));
    this.requestQueue = [];
  }

  handleAuthFailure() {
    const userStore = useUserStore();
    userStore.clearAuth();

    // Emit event for components to handle
    window.dispatchEvent(new CustomEvent('auth:required'));
  }
}

// Export singleton instance
export const apiClient = new AuthInterceptor();

// Convenience wrapper for authenticated API calls
export const api = {
  get: (url, options) => apiClient.get(url, options),
  post: (url, body, options) => apiClient.post(url, body, options),
  put: (url, body, options) => apiClient.put(url, body, options),
  delete: (url, options) => apiClient.delete(url, options),
};