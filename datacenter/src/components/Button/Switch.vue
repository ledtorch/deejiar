<template>
  <div class="switch-container flex-col">
    <div class="nav">
      <p class="_subtitle the-title">{{ title }}</p>
    </div>
    <div class="dj-switch-group" role="tablist" aria-label="binary toggle">
      <button role="tab" :aria-selected="isLeft.toString()" class="seg" :class="{ active: isLeft }" @click="selectLeft"
        @keydown.enter.prevent="selectLeft" @keydown.space.prevent="selectLeft">
        {{ leftText }}
      </button>

      <button role="tab" :aria-selected="(!isLeft).toString()" class="seg" :class="{ active: !isLeft }"
        @click="selectRight" @keydown.enter.prevent="selectRight" @keydown.space.prevent="selectRight">
        {{ rightText }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const emit = defineEmits(['update:modelValue', 'change', 'left', 'right'])

const props = defineProps({
  modelValue: { type: Boolean, default: true }, // true => left active, false => right active
  leftText: { type: String, default: 'food' },
  rightText: { type: String, default: 'view' },
  title: { type: String, default: '?' },
})

const isLeft = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

function selectLeft() {
  if (!isLeft.value) {
    isLeft.value = true
    emit('change', true)
    emit('left') // function1 hook
  }
}

function selectRight() {
  if (isLeft.value) {
    isLeft.value = false
    emit('change', false)
    emit('right') // function2 hook
  }
}
</script>

<style scoped lang="scss">
.dj-switch-group {
  height: 46px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px;
  border-radius: 6px;
  background: var(--base);
}

.seg {
  appearance: none;
  border: 0;
  cursor: pointer;
  padding: 8px 14px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 14px;
  line-height: 1;
  background: transparent;
  color: var(--secondary-text);
}

.seg.active {
  background: #000;
  /* active background */
  color: #fff;
  /* active text */
}

/* Focus ring for accessibility */
.seg:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, .45);
}

.nav {
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
  height: 24px;
}

.the-title {
  padding: 0px 4px;
  color: var(--secondary-text);
}

.switch-container {
  width: 100%;
  gap: 4px;
}
</style>
