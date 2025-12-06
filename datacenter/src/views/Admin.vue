<template>
  <main class="page">
    <section class="dashboard-frame">
      <form class="submit-frame" @submit.prevent="submitLogin">

        <fieldset class="form-frame">
          <p class="_subtitle the-title">Username</p>
          <input :class="{ input: !editing, 'input-on': editing }" id="account" type="text"
            v-model="credentials.username" />
        </fieldset>

        <fieldset class="form-frame">
          <p class="_subtitle the-title">Password</p>
          <input :class="{ input: !editing, 'input-on': editing }" id="password" type="password"
            v-model="credentials.password" />
        </fieldset>

        <PrimaryButton type="submit" class="text-color" label="Login" />
      </form>
    </section>
  </main>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PrimaryButton from '../components/buttons/Primary.vue'

const router = useRouter()
defineOptions({ name: 'TheAdm' })

// State
const credentials = ref({
  username: '',
  password: ''
})
// Initially not in editing mode for css
const editing = ref(false)
// Router


// Token timer
function startSessionTimer() {
  setTimeout(() => {
    console.log('Session expired')
    localStorage.removeItem('access_token')
    router.push('/')
  }, 3600000) // 60min
}

// Actions
async function submitLogin() {
  try {
    // Link to the FastAPI
    const apiUrl = import.meta.env.VITE_DATACENTER_API
    console.log(apiUrl)
    const response = await axios.post(`${apiUrl}/admin/auth/login`, credentials.value)
    localStorage.setItem('access_token', response.data.access_token)


    // 🐞 Debug console
    console.log('Login successful:', response.data)
    console.log('API URL:', import.meta.env.VITE_DATACENTER_API)

    // Start the session timer after successful login
    startSessionTimer()


    router.push('/dashboard')
  } catch (error) {
    if (error?.response) {
      console.error('Login failed:', error.response.data)
    } else {
      console.error('Login failed: Network error or CORS issue')
    }
  }
}
</script>

<style lang="scss" scoped>
.page {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100vw;
  height: 100%;
}

.dashboard-frame {
  flex-direction: column;
  align-items: flex-start;
  align-items: center;
  gap: var(--container);
}

.submit-frame {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--container);
}

.form-frame {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  height: fit-content;
  gap: var(--atom);
  border: none;
  padding: 0;
}

.the-title {
  height: 24px;
  color: var(--secondary-text);
}

.input {
  width: auto;
  padding: 12px;
  border: 0px;
  border-radius: var(--border-content);
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
  background-color: var(--base);
}

.input-on {
  width: auto;
  padding: 12px;
  border: 1px solid var(--baseline-green);
  border-radius: var(--border-content);
  box-sizing: border-box;
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}

.hide {
  display: none;
}

.text-color {
  color: var(--primary-text);
}
</style>