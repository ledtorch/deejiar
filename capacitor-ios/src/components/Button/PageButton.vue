<template>
  <button :class="[
    'icon-button',
    {
      'is-pressed': isPressed,
      'is-disabled': disabled
    }
  ]" :disabled="disabled" @pointerdown="onPressStart" @pointerup="onPressEnd" @click="handleClick">
    <img v-if="iconSrc" :src="iconSrc" class="icon" />

    <p v-if="props.action" class="button-label _button-secondary">{{ props.action }}</p>
  </button>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  action: { type: String, default: '' },
  icon: { type: String, default: '' },
  disabled: { type: Boolean, default: false },
  // Boolean props for different types
  inbox: { type: Boolean, default: false },
  map: { type: Boolean, default: false },
  help: { type: Boolean, default: false }
})

const emit = defineEmits(['click'])

const isPressed = ref(false)

// Icon mapping
const iconMap = {
  'inbox': '/icon/action/email.svg',
  'map': '/icon/action/map.svg',
  'help': '/icon/action/help.svg'
}

// Computed icon source - check boolean props first, then icon prop
const iconSrc = computed(() => {
  // Check boolean props first
  if (props.inbox) return iconMap.inbox
  if (props.map) return iconMap.map
  if (props.help) return iconMap.help

  // Fallback to icon prop
  if (props.icon && iconMap[props.icon]) {
    return iconMap[props.icon]
  }

  return iconMap.inbox // Default fallback
})

const onPressStart = () => {
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
.icon-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--unit);

  background: none;
  border: none;
  cursor: pointer;
  padding: var(--box);

  width: 100%;
  height: 90px;

  border-radius: var(--round-m);
  transition: all 0.2s ease;

  background: var(--gray-button);
}

.icon {
  width: 36px;
  height: 36px;
  object-fit: contain;
  filter: opacity(0.3);
}

.button-label {
  color: var(--primary-text);
  text-align: center;
  filter: opacity(0.3);
}
</style>