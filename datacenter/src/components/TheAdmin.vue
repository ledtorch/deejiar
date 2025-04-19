<template>
  <div class="body">
    <div class="dashboard-frame">
      <h1>Datacenter</h1>

      <form class="submit-frame" @submit.prevent="submitLogin">

        <div class="form-frame">
          <div class="nav">
            <p class="headline">Account</p>
          </div>
          <input :class="{ input: !editing, 'input-on': editing }" id="account" type="text"
            v-model="credentials.username" />
        </div>

        <div class="form-frame">
          <div class="nav">
            <p class="headline">Password</p>
          </div>
          <input :class="{ input: !editing, 'input-on': editing }" id="password" type="password"
            v-model="credentials.password" />
        </div>

        <button type="submit" class="temp-button">Login</button>
      </form>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'TheAdm',
  data() {
    return {
      credentials: {
        // 🏗️ TODO: should update "account" to "username"
        username: '',
        password: ''
      },
      // Initially not in editing mode for css
      editing: false,
    }
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  methods: {
    // Token timer
    startSessionTimer() {
      setTimeout(() => {
        console.log('Session expired');
        localStorage.removeItem('access_token');
        this.router.push('/');
      }, 3600000); // 60min
    },

    async submitLogin() {
      try {
        // Link to the Flask 
        const apiUrl = import.meta.env.VITE_DATACENTER_API;
        const response = await axios.post(`${apiUrl}/login`, this.credentials);
        localStorage.setItem('access_token', response.data.access_token);

        // 🐞 Debug console
        console.log('Login successful:', response.data);
        console.log('API URL:', import.meta.env.VITE_DATACENTER_API);

        // Start the session timer after successful login
        this.startSessionTimer();

        this.router.push('/dashboard');
      } catch (error) {
        if (error.response) {
          console.error('Login failed:', error.response.data);
        } else {
          console.error('Login failed: Network error or CORS issue');
        }
      }
    }

  }
}
</script>

<style lang="scss" scoped>
.body {
  flex-direction: column;
  align-items: center;
  padding: 80px;
  width: 100vw;
  height: 100%;
}

.dashboard-frame {
  flex-direction: column;
  align-items: flex-start;
  gap: 24px;
}

.nav {
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}

.submit-frame {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 24px;
}

.form-frame {
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  gap: 4px;
}

.headline {
  font-size: 16px;
  font-weight: 500;
  line-height: 21px;
  color: var(--3-text-dark-2nd-white,
      var(--token-secondary-text, rgba(255, 255, 255, 0.75)));
}

.input {
  width: auto;
  padding: 12px;
  border: 0px;
  border-radius: var(--border-content, 6px);
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}

.input-on {
  width: auto;
  padding: 12px;
  border: 1px solid var(--baseline-green, #3dc363);
  border-radius: var(--border-content, 6px);
  box-sizing: border-box;
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}

.hide {
  display: none;
}

.temp-button {
  cursor: pointer;
  background-color: transparent;
  border: 0px;
  padding: 10px 16px;
  justify-content: center;
  align-items: center;
  border-radius: var(--border-button-round, 8px);
  background: var(--token-theme, #fafafa);
  color: var(--token-invert, #0e0d0f);

  font-family: Be Vietnam Pro;
  font-size: 15px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;
}
</style>