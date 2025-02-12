<template>
  <button class="icon-button"></button>
</template>

<script>
export default {
  name: 'Home'
};
</script>

<style lang="scss" scoped>
.icon-button {
  cursor: pointer;
  width: 32px;
  height: 32px;
  background: no-repeat center/contain;
  background-image: url("/button/icon/with-base/home-default.png");

  // 🏗️ TODO: Doesn't work
  &:active {
    background-image: url("/button/icon/with-base/home-click.png");
  }

  &:hover {
    background-image: url("/button/icon/with-base/home-hover.png");
  }

  &:disabled {
    cursor: not-allowed;
    background-image: url("/button/icon/with-base/home-inactive.png");
  }
}
</style>
