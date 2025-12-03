<template>
  <button class="icon-button" @click="onClick"></button>
</template>

<script>
export default {
  name: 'Locate',
  methods: {
    onClick() {
      this.$emit("locate");
    },
  },
};
</script>

<style lang="scss" scoped>
.icon-button {
  cursor: pointer;
  width: 40px;
  height: 40px;
  background: no-repeat center/contain;
  background-image: url("/button/icon/with-base/locate-default.png");

  &:active {
    background-image: url("/button/icon/with-base/locate-click.png");
  }

  // 🏗️ TODO: Added will cover the active(click) effect
  // &:hover {
  //   background-image: url("/button/icon/with-base/locate-hover.png");
  // }

  &:disabled {
    cursor: not-allowed;
    background-image: url("/button/icon/with-base/locate-inactive.png");
  }
}
</style>
