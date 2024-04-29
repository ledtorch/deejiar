<template>
  <button class="icon-button"></button>
</template>

<script>
export default {
  name: 'Like'
};
</script>

<style lang="scss" scoped>
.icon-button {
  cursor: pointer;
  width: 32px;
  height: 32px;
  background: no-repeat center/contain;
  background-image: url("/button/icon/with-base/like-default.png");

  // 🏗️ TODO: Doesn't work
  &:active {
    background-image: url("/button/icon/with-base/like-click.png");
  }

  &:hover {
    background-image: url("/button/icon/with-base/like-hover.png");
  }

  &:disabled {
    cursor: not-allowed;
    background-image: url("/button/icon/with-base/like-inactive.png");
  }
}
</style>
