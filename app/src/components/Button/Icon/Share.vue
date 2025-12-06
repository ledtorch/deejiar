<template>
  <button class="icon-button"></button>
</template>

<script setup>
</script>

<style lang="scss" scoped>
.icon-button {
  cursor: pointer;
  width: 32px;
  height: 32px;
  background: no-repeat center/contain;
  background-image: url("/button/icon/with-base/share-default.png");

  // 🏗️ TODO: Doesn't work
  &:active {
    background-image: url("/button/icon/with-base/share-click.png");
  }

  &:hover {
    background-image: url("/button/icon/with-base/share-hover.png");
  }

  &:disabled {
    cursor: not-allowed;
    background-image: url("/button/icon/with-base/share-inactive.png");
  }
}
</style>
