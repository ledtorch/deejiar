<template>
  <div class="search-wrapper _stretch" :style="wrapperStyle">
    <div class="search-field" :class="{ focused: isFocused }">
      <div class="search-icon"></div>

      <input class="search-input caption1" :placeholder="placeholder" type="search" :autofocus="autofocus"
        :value="localValue" @input="onInput" @focus="isFocused = true" @blur="isFocused = false"
        @keydown.enter="emit('submit', localValue)" aria-label="Search" />
    </div>
  </div>

</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: 'Search' },
  autofocus: { type: Boolean, default: false },
  // Allow consumer to override outer spacing without breaking parent flex
  margin: { type: String, default: '0' }
})

const emit = defineEmits(['update:modelValue', 'submit'])

const localValue = ref(props.modelValue)
watch(
  () => props.modelValue,
  (val) => {
    if (val !== localValue.value) localValue.value = val ?? ''
  }
)

const onInput = (e) => {
  localValue.value = e.target.value
  emit('update:modelValue', localValue.value)
}

const isFocused = ref(false)

const wrapperStyle = computed(() => ({
  margin: props.margin,
  width: '100%'
}))
</script>

<style lang="scss" scoped>
.search-wrapper {
  width: 100%;
}

.search-field {
  /* Fill available width from parent flex column */
  width: 100%;
  height: 36px;
  padding: 6px 8px;
  border-radius: 8px;
  background: var(--button-base);
  align-items: center;
  gap: 4px;
  transition: background 120ms ease, box-shadow 120ms ease;
}

.search-field.focused {
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.14) inset;
}

.search-icon {
  width: 24px;
  height: 24px;
  flex: 0 0 auto;
  cursor: pointer;
  background: no-repeat center/contain;
  background-size: 24px;
  background-image: url("/button/icon/control-data/search-defaul.png");

  &:active {
    background-image: url("/button/icon/control-data/search-click.png");
  }

  &:hover {
    background-image: url("/button/icon/control-data/search-hover.png");
  }

  &:disabled {
    cursor: not-allowed;
    background-image: url("/button/icon/control-data/search-inactive.png");
  }
}

.search-input {
  flex: 1 1 auto;
  background: transparent;
  border: none;
  outline: none;
  color: var(--secondary-text);
  caret-color: var(--silver);
}

.search-input::placeholder {
  color: var(--tertiary-text)
}
</style>