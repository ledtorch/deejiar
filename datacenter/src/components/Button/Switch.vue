<template>
  <button class="dj-switch" role="switch" :aria-checked="isOn.toString()" :class="{ 'is-on': isOn, 'is-off': !isOn }"
    @click="toggle" @keydown.space.prevent="toggle" @keydown.enter.prevent="toggle">
    <span class="label" v-if="label">{{ label }}</span>
    <span class="state-text">{{ isOn ? trueText : falseText }}</span>
    <span class="track">
      <span class="thumb" />
    </span>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const emit = defineEmits(['update:modelValue', 'change'])

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  label: { type: String, default: '' },
  trueText: { type: String, default: 'True' },
  falseText: { type: String, default: 'False' },
})

const isOn = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

function toggle() {
  const next = !isOn.value
  isOn.value = next
  emit('change', next)
}
</script>

<style scoped lang="scss">
.dj-switch {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 999px;
  border: 0;
  cursor: pointer;
  user-select: none;
  outline: none;
  background: #000;
  /* black background to match the mock */
  color: #fff;
  /* white text to match the mock */
  font-weight: 600;
  font-size: 14px;
  line-height: 1;
}

.dj-switch .label {
  opacity: 0.8;
}

.dj-switch .state-text {
  min-width: 34px;
  /* keeps width stable between True/False */
  text-align: left;
}

.dj-switch .track {
  width: 42px;
  height: 24px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.18);
  position: relative;
  flex-shrink: 0;
}

.dj-switch .thumb {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #fff;
  transition: transform 160ms ease;
}

.dj-switch.is-on .thumb {
  transform: translateX(18px);
}

.dj-switch:focus-visible {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, .45);
  /* accessible focus ring */
}
</style>
