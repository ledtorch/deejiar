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
            v-model="credentials.account" />
        </div>

        <div class="form-frame">
          <div class="nav">
            <p class="headline">Password</p>
          </div>
          <input :class="{ input: !editing, 'input-on': editing }" id="password" type="password"
            v-model="credentials.password" />
        </div>



        <button type="submit">Login</button>



      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router'; // Import useRouter

export default {
  name: 'TheAdm',
  data() {
    return {
      credentials: {
        account: '',
        password: ''
      },
      editing: false, // Assuming you have some logic for this
    }
  },
  setup() {
    const router = useRouter(); // Use useRouter to access the router instance
    return { router };
  },
  methods: {
    async submitLogin() { // Updated to match the @submit.prevent
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', this.credentials);
        console.log('Login successful:', response.data);
        // Store the JWT in local storage
        localStorage.setItem('access_token', response.data.access_token);
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
</style>