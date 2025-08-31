<template>
  <!-- Divider: or -->
  <div v-if="or" class="divider-or-container">
    <div class="divider-horizontal" />
    <span class="_caption1 _color-secondary">or</span>
    <div class="divider-horizontal" />
  </div>

  <!-- Dividers: horizontal or vertical -->
  <div v-else :class="dividerType" />
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  vertical: {
    type: Boolean,
    default: false
  },
  or: {
    type: Boolean,
    default: false
  }
})

const dividerType = computed(() =>
  props.vertical ? 'divider-vertical' : 'divider-horizontal'
)
</script>

<style lang="scss" scoped>
.divider-horizontal {
  width: 100%;
  min-height: 1px;
  background: var(--tertiary-text);
  opacity: 0.2;
}

.divider-vertical {
  width: 1px;
  min-height: 100%;
  background: var(--tertiary-text);
  opacity: 0.2;
}

.divider-or-container {
  display: flex;
  align-items: center;
  width: 100%;
  gap: var(--atom);
  padding: 0 var(--atom);
}
</style>