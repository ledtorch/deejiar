<template>
  <div class="dropdown-container" :class="{ 'is-open': isOpen }">
    <button class="dropdown-trigger" @click="toggle">
      <span class="dropdown-label">{{ selectedLabel || placeholder }}</span>
    </button>

    <div v-if="isOpen" class="dropdown-menu">
      <button v-for="option in options" :key="option.value" class="dropdown-option"
        :class="{ 'selected': option.value === selected }" @click="selectOption(option)">
        {{ option.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  options: Array,
  placeholder: String,
  modelValue: [String, Number]
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const selected = computed(() => props.modelValue)

const selectedLabel = computed(() => {
  const option = props.options.find(opt => opt.value === selected.value)
  return option?.label
})

const toggle = () => {
  isOpen.value = !isOpen.value
}

const selectOption = (option) => {
  emit('update:modelValue', option.value)
  isOpen.value = false
}
</script>