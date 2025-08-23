<template>
  <section class="switch-container flex-col" aria-labelledby="switch-title">
    <header class="nav">
      <p id="switch-title" class="_subtitle the-title">{{ title }}</p>
    </header>

    <div class="button-set-container" role="tablist" :aria-label="title || 'binary toggle'">
      <button type="button" role="tab" :aria-selected="isLeft.toString()" :tabindex="isLeft ? 0 : -1" class="seg"
        :class="{ active: isLeft }" @click="selectLeft" @keydown.enter.prevent="selectLeft"
        @keydown.space.prevent="selectLeft">
        {{ leftText }}
      </button>

      <button type="button" role="tab" :aria-selected="(!isLeft).toString()" :tabindex="!isLeft ? 0 : -1" class="seg"
        :class="{ active: !isLeft }" @click="selectRight" @keydown.enter.prevent="selectRight"
        @keydown.space.prevent="selectRight">
        {{ rightText }}
      </button>
    </div>
  </section>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const emit = defineEmits(['update:modelValue', 'change', 'left', 'right'])

const props = defineProps({
  modelValue: { type: Boolean, default: undefined },
  leftText: { type: String, default: 'food' },
  rightText: { type: String, default: 'view' },
  title: { type: String, default: '?' },
})

// Local fallback state for uncontrolled usage
const inner = ref(typeof props.modelValue === 'boolean' ? props.modelValue : true)

// If parent controls it (v-model), mirror changes into local state for visual consistency
watch(
  () => props.modelValue,
  (val) => {
    if (typeof val === 'boolean') inner.value = val
  }
)

const isLeft = computed({
  get: () => (typeof props.modelValue === 'boolean' ? props.modelValue : inner.value),
  set: (val) => {
    inner.value = val
    // Notify parent if they are controlling it
    emit('update:modelValue', val)
  },
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
.button-set-container {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 46px;
  width: 100%;
  padding: 4px;
  border-radius: 6px;
  background: var(--base);
}

.seg {
  flex: 1 0 0;
  width: 100%;
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
  display: flex;
  justify-content: center;
  /* Center text horizontally */
  align-items: center;
  /* Center text vertically */
  flex: 1 0 0;
  height: 38px;
  width: 100%;

  padding: 7px var(--Layout-Block, 12px);

  border-radius: var(--Round-S, 4px);

  background: var(--Color-Primary, rgba(0, 0, 0, 0.95));

  color: #fff;
  font-weight: 700;

  cursor: pointer;
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
