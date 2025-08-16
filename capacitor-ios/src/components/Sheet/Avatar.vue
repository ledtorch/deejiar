<template>
  <button class="icon-button" @click="loginWithTwitter" :style="buttonStyle" />
</template>

<script setup>
import { computed } from 'vue'

const buttonStyle = computed(() => ({
  backgroundImage: "url('/icon/avatar.png')",
}))

const loginWithTwitter = () => {
  // Implement auth or replace with desired behavior
  console.log('Login with Twitter clicked')
}
</script>

<style lang="scss" scoped>
.icon-button {
  cursor: pointer;
  width: 36px;
  height: 36px;
  background: no-repeat center/contain;
  transition: transform 0.2s ease;
}
</style>
