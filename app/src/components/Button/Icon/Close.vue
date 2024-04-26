<template>
  <button class="icon-button" @click="onClick"></button>
</template>

<script>
export default {
  name: 'Close',
  methods: {
    onClick() {
      this.$emit("close");
    },
  }
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
  background-image: url("/button/icon/with-base/close-default.png");

  // 🏗️ TODO: Doesn't work
  &:active {
    background-image: url("/button/icon/with-base/close-click.png");
  }

  &:hover {
    background-image: url("/button/icon/with-base/close-hover.png");
  }

  &:disabled {
    cursor: not-allowed;
    background-image: url("/button/icon/with-base/close-inactive.png");
  }
}
</style>
