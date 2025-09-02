<template>
  <section class="search-container">
    <div class="search-component">
      <TheSearch />
      <TheAvatar class="avatar-layout" userState="default" uphoto="..." uid="..." :useBottomSheet="true" />
    </div>
  </section>
</template>

<script setup>
import TheSearch from '../../TheSearch.vue';
import TheAvatar from '../../button/TheAvatar.vue';
</script>

<style lang="scss" scoped>
.search-container {
  display: flex;
  flex-direction: column;
  padding: 0 var(--wrapper);
}

.search-component {
  justify-content: space-between;
  gap: var(--block);
}

.avatar-layout {
  width: 36px;
  height: 36px;
}
</style>