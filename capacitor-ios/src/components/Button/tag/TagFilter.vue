<template>
  <section class="tag-container">
    <div class="tag-title">
      <img :src="iconSrc" class="tag-icon" />
      <p v-if="props.action" class="tag-text _button-primary">{{ text }} Text</p>
      <p v-else class="tag-text _button-primary">Test Text</p>
    </div>
    <Close type="item" @close="handleClose" />
  </section>
</template>

<script setup>
import { computed } from 'vue'
import Close from '../Icon/Close.vue'

const props = defineProps({
  icon: {
    type: String,
    required: true
  },
  text: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close'])

const iconSrc = computed(() => {
  // Handle both full paths and icon names
  if (props.icon.startsWith('/') || props.icon.startsWith('http')) {
    return props.icon
  } else {
    return `/icon/logo/logo.png`
  }
})

const handleClose = () => {
  emit('close')
}
</script>

<style lang="scss" scoped>
.tag-container {
  cursor: pointer;

  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--unit);

  padding: var(--atom) var(--atom) var(--atom) var(--unit);
  border-radius: var(--round-m);

  width: fit-content;
  height: 32px;

  transition: all 0.2s ease;

  background: var(--primary-text);
}

.tag-title {
  display: flex;
  align-items: center;
  gap: var(--atom);
}

.tag-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.tag-text {
  color: var(--invert-primary);
}
</style>