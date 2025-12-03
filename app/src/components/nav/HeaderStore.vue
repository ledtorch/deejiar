<template>
  <div class="header-store">
    <h4 class="store-title">{{ store.title }}</h4>
    <TagShopType :store="store" />
  </div>
</template>

<script setup>
import TagShopType from '../button/TagShopType.vue';

const props = defineProps({
  store: { type: Object, default: () => ({}) }
})
</script>

<style lang="scss" scoped>
.header-store {
  width: 100%;
  align-items: top;
  justify-content: space-between;
  gap: var(--block);
}

.store-title {
  flex: 1 0 0;
}
</style>