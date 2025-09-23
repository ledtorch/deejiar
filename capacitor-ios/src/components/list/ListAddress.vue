<template>
  <div class="list-container">
    <img :src="iconSrc" class="icon">
    <p class="_body2 address-text">{{ address }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import iconAddressLight from '@/assets/icons/store-info/address-light.svg'
import iconAddressDark from '@/assets/icons/store-info/address-dark.svg'

const props = defineProps({
  address: String
});

const iconSrc = computed(() => {
  return iconAddressDark
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
