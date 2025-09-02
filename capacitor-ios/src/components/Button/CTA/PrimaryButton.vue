<template>
  <button v-if="default" :class="['button-container', '_button-secondary', { 'is-pressed': isPressed }]"
    @pointerdown="onPressStart" @pointerup="onPressEnd">{{ action }}</button>

  <button v-else-if="iconLeft" :class="['button-container', '_button-secondary', { 'is-pressed': isPressed }]"
    @pointerdown="onPressStart" @pointerup="onPressEnd"><img src="/icon/social/instagram-color.png"
      class="action-icon" />{{ action }}</button>

  <button v-else-if="iconRight" :class="['button-container', '_button-secondary', { 'is-pressed': isPressed }]"
    @pointerdown="onPressStart" @pointerup="onPressEnd">{{ action }}<img src="/icon/social/instagram-color.png"
      class="action-icon" /></button>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  action: { type: String, default: '' },
  default: { type: Boolean, default: false },
  iconLeft: { type: Boolean, default: false },
  iconRight: { type: Boolean, default: false },
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
  min-height: 44px;
  padding: 0 var(--division);
  gap: var(--atom);
  border-radius: var(--round-m);
  background: var(--primary-text);
  color: var(--invert-primary);

  /* Interactions */
  transition: all 0.3s ease;

  &.is-pressed {
    background: var(--tertiary-text);
  }
}

.action-icon {
  width: 24px;
  height: 24px;
}
</style>
