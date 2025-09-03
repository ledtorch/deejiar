<template>
  <div class="header-store">
    <p class="_title product-name">{{ product.name }}</p>
    <p class="_title product-price">{{ product.price }}</p>
  </div>
</template>

<script setup>

const props = defineProps({
  product: { type: Object, default: () => ({}) }
})
</script>

<style lang="scss" scoped>
.header-store {
  width: 100%;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.product-name {
  width: 100%;
  align-items: center;
  justify-content: space-between;
}

.product-price {
  flex: 1 0 0;
}
</style>
