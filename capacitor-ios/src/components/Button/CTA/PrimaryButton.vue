<template>
  <button :class="[
    'button-container',
    '_button-secondary',
    {
      'is-pressed': isPressed,
      'is-disabled': disabled,
      'has-icon-left': type === 'icon-left' && iconSrc,
      'has-icon-right': type === 'icon-right' && iconSrc
    }
  ]" :disabled="disabled" @pointerdown="onPressStart" @pointerup="onPressEnd" @click="handleClick">
    <!-- Left icon -->
    <img v-if="type === 'icon-left' && iconSrc" :src="iconSrc" class="action-icon" />

    <!-- Button text -->
    <span class="button-text">{{ action }}</span>

    <!-- Right icon -->
    <img v-if="type === 'icon-right' && iconSrc" :src="iconSrc" class="action-icon" />
  </button>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  action: { type: String, default: '' },
  type: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'icon-left', 'icon-right'].includes(value)
  },
  icon: { type: String, default: '' }, // Icon name: 'arrow-left', 'arrow-right', 'instagram', etc.
  disabled: { type: Boolean, default: false }
})

const emit = defineEmits(['click'])

const isPressed = ref(false)

// Icon mapping
const iconMap = {
  'arrow-left': '/button/icon/control-data/arrow-left.svg',
  'arrow-right': '/button/icon/control-data/arrow-right.svg',
  'instagram': '/icon/social/instagram-color.png',
  'x': '/icon/social/x-color.png',
  // Add more icons as needed
}

// Computed icon source
const iconSrc = computed(() => {
  if (props.icon && iconMap[props.icon]) {
    return iconMap[props.icon]
  }
  return ''
})

const onPressStart = (e) => {
  if (!props.disabled) {
    isPressed.value = true
  }
}

const onPressEnd = () => {
  isPressed.value = false
}

const handleClick = (event) => {
  if (!props.disabled) {
    emit('click', event)
  }
}
</script>

<style lang="scss" scoped>
.button-container {
  display: flex;
  align-self: stretch;
  align-items: center;
  justify-content: center;
  width: auto;
  min-height: 42px;
  margin: 1 0;
  gap: var(--atom);
  border-radius: var(--round-m);
  background: var(--primary-text);
  color: var(--invert-primary);
  border: none;
  cursor: pointer;

  /* Default padding (no icon) */
  padding: 0 var(--division);

  /* Icon left: extra padding on left side */
  &.has-icon-left {
    padding-left: var(--box);
    padding-right: var(--division);
  }

  /* Icon right: extra padding on right side */
  &.has-icon-right {
    padding-left: var(--division);
    padding-right: var(--box);
  }

  /* Interactions */
  transition: all 0.3s ease;

  &.is-pressed {
    background: var(--tertiary-text);
  }

  &.is-disabled {
    background: var(--tertiary-text);
    color: var(--secondary-text);
    cursor: not-allowed;
    opacity: 0.6;
  }
}

.action-icon {
  width: 24px;
  height: 24px;
}

.has-icon-left {
  padding: 0 var(--division) 0 var(--block);
}

.has-icon-right {
  padding: 0 var(--block) 0 var(--division);
}
</style>
