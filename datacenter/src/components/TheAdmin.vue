<template>
  <main class="body flex">
    <section class="dashboard-frame">
      <form class="submit-frame" @submit.prevent="submitLogin">

        <fieldset class="form-frame">
          <p class="_subtitle _color-secondary the-title">Account</p>
          <input :class="{ input: !editing, 'input-on': editing }" id="account" type="text"
            v-model="credentials.username" />
        </fieldset>

        <fieldset class="form-frame">
          <p class="_subtitle _color-secondary the-title">Password</p>
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
import PrimaryButton from './Button/Primary.vue'

defineOptions({ name: 'TheAdm' })

// State
const credentials = ref({
  // 🏗️ TODO: should update "account" to "username"
  username: '',
  password: ''
})
// Initially not in editing mode for css
const editing = ref(false)
// Router
const router = useRouter()

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
    const response = await axios.post(`${apiUrl}/admin/login`, credentials.value)
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
  align-items: center;
  gap: 24px;
}

.submit-frame {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 24px;
}

.form-frame {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  gap: 4px;
  border: none;
  padding: 0;
}

.the-title {
  height: 24px;
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

.text-color {

  color: #fff;
}
</style>