<template>
  <button class="icon-button"></button>
</template>

<script>
export default {
  name: 'HomeToDetailCover'
};
</script>

<style lang="scss" scoped>
.icon-button {
  cursor: pointer;
  width: 32px;
  height: 32px;
  background: no-repeat center/contain;
  background-image: url("/button/icon/with-base/home-detail-default.png");

  // 🏗️ TODO: Doesn't work
  &:active {
    background-image: url("/button/icon/with-base/home-detail-click.png");
  }

  &:hover {
    background-image: url("/button/icon/with-base/home-detail-hover.png");
  }

  &:disabled {
    cursor: not-allowed;
    background-image: url("/button/icon/with-base/home-detail-inactive.png");
  }
}
</style>
