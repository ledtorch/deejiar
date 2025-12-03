<template>
  <button v-if="instagram" :class="['button-container', '_button-secondary', { 'is-pressed': isPressed }]"
    @pointerdown="onPressStart" @pointerup="onPressEnd">
    <img src="/icon/social/instagram-color.png" class="auth-icon" />
    {{ action }}</button>

  <button v-else-if="x" :class="['button-container', '_button-secondary', { 'is-pressed': isPressed }]"
    @pointerdown="onPressStart" @pointerup="onPressEnd">
    <img src="/icon/social/x-color.png" class="auth-icon" />
    {{ action }}</button>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  action: { type: String, default: '' },
  instagram: { type: Boolean, default: false },
  x: { type: Boolean, default: false },
})

const isPressed = ref(false)

const onPressStart = (e) => {
  isPressed.value = true;
};
const onPressEnd = () => {
  isPressed.value = false;
};

</script>

<style lang="scss" scoped>
.button-container {
  display: flex;
  align-self: stretch;
  align-items: center;
  justify-content: center;
  width: auto;
  height: 44px;
  padding: 0 var(--division);
  gap: var(--atom);
  border-radius: var(--round-m);
  background: var(--content);
  color: var(--primary-text);

  /* Interactions */
  transition: all 0.3s ease;

  &.is-pressed {
    background: transparent;
  }
}

.auth-icon {
  width: 24px;
  height: 24px;
}
</style>
