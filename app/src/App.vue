<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useATT } from './composables/useATT'

const { requestPermission, isIOS } = useATT()

onMounted(async () => {
  if (isIOS()) {
    // Wait 1 second for app to become active
    setTimeout(async () => {
      console.log('[ATT] Requesting permission...')
      const result = await requestPermission()
      console.log('[ATT] Result:', result)
    }, 1000)
  }
})
</script>