<template>
  <button class="icon-button"></button>
</template>

<script>
export default {
  name: 'LeftArrow'
};
</script>

<style lang="scss" scoped>
.icon-button {
  cursor: pointer;
  width: 32px;
  height: 32px;
  border: none;
  padding: 0;
  background: no-repeat center/contain;
  background-image: url("/button/icon/with-base/left-arrow-default.png");

  // 🏗️ TODO: Doesn't work
  &:active {
    background-image: url("/button/icon/with-base/left-arrow-click.png");
  }

  &:hover {
    background-image: url("/button/icon/with-base/left-arrow-hover.png");
  }

  &:disabled {
    cursor: not-allowed;
    background-image: url("/button/icon/with-base/left-arrow-inactive.png");
  }
}
</style>
