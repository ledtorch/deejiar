<template>
  <div class="list-container">
    <img :src="iconSrc" class="icon icon-themed">
    <p class="_body2 address-text">{{ address }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import iconAddress from '@/assets/icons/store-info/address.svg'

const props = defineProps({
  address: String
});

const iconSrc = computed(() => {
  return iconAddress
})
</script>


<style lang="scss" scoped>
.list-container {
  align-items: flex-start;
  gap: var(--unit);
  align-self: stretch;
}

.icon {
  min-width: 20px;
  height: 20px;
}

.address-text {
  color: var(--primary-text);
}
</style>
