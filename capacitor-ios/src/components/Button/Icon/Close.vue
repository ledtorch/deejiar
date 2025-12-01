<template>
  <button :class="buttonClass + ' icon-themed'" @click="onClick"></button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'item',
    validator: (value) => ['item', 'modal'].includes(value)
  }
})

const emit = defineEmits(['close'])

const buttonClass = computed(() => {
  return props.type === 'modal' ? 'close-modal' : 'close-item'
})

const onClick = () => {
  emit('close')
}
</script>

<style lang="scss" scoped>
.close-item {
  cursor: pointer;
  min-width: 24px;
  min-height: 24px;
  background: no-repeat center/contain;
  background-image: url("/button/icon/control/close-item.svg");
}

.close-modal {
  cursor: pointer;
  min-width: 32px;
  min-height: 32px;
  background: no-repeat center/contain;
  background-image: url("/button/icon/with-base/close-default.png");
}
</style>
