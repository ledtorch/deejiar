<template>
  <main class="launch-screen">
    <div class="logo-container">
      <lottie-player v-if="!useFallback" ref="lottiePlayerRef" autoplay mode="normal" :src="animationSrc"
        class="loading-animation" @error="handleError" />
      <img v-else src="/icon/logo/loading.gif" alt="Loading..." class="loading-animation" />
      <h4 class="app-name">Deejiar</h4>
    </div>
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import "@lottiefiles/lottie-player";

const router = useRouter()
const lottiePlayerRef = ref(null)
const useFallback = ref(false)
const animationSrc = '/icon/logo/loading.json'

const handleError = () => {
  useFallback.value = true
}

onMounted(() => {
  setTimeout(() => {
    router.replace('/map')
  }, 1600)
})
</script>

<style scoped>
.launch-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.loading-animation {
  width: 90px;
  height: 90px;
}

.app-name {
  color: #fff;
  margin: 0;
}
</style>