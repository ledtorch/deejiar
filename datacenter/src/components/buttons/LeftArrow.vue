<template>
  <button class="icon-button"></button>
</template>

<style lang="scss" scoped>
.icon-button {
  cursor: pointer;
  width: 24px;
  height: 24px;
  background: no-repeat center/contain;
  background-image: url("/button/icon/contral-data/left-arrow-default.png");

  // 🏗️ TODO: Doesn't work
  &:active {
    background-image: url("/button/icon/contral-data/left-arrow-click.png");
  }

  &:hover {
    background-image: url("/button/icon/contral-data/left-arrow-hover.png");
  }

  &:disabled {
    cursor: not-allowed;
    background-image: url("/button/icon/contral-data/left-arrow-inactive.png");
  }
}
</style>
