<template>
  <div class="header-store">
    <h5 class="product-name">{{ product.name }}</h5>
    <h5 class="product-price">{{ product.price }}</h5>
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
  align-items: top;
  justify-content: space-between;
  flex-wrap: wrap;
}

.product-name {
  width: 100%;
  align-items: center;
  justify-content: space-between;
  flex: 1 0 0;
}
</style>
