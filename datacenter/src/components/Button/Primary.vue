<template>
  <button class="button-container _button-secondary">{{ label }}</button>
</template>

<script setup>
const props = defineProps({
  label: { type: String, default: '' },
})
</script>

<style lang="scss" scoped>
.button-container {
  display: flex;
  width: auto;
  height: 42px;
  padding: 10px 16px;
  justify-content: center;
  gap: 4px;
  align-self: stretch;
  border-radius: var(--Round-M, 8px);
  background: rgba(0, 0, 0, 0.95);
}
</style>
