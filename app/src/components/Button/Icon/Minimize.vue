<template>
  <button class="icon-button" @click="onClick"></button>
</template>

<script>
export default {
  name: 'Minimize',
  methods: {
    onClick() {
      this.$emit("minimize");
    },
  }
};
</script>

<style lang="scss" scoped>
.icon-button {
  cursor: pointer;
  width: 32px;
  height: 32px;
  background: no-repeat center/contain;
  background-image: url("/button/icon/with-base/minimize-default.png");

  // 🏗️ TODO: Doesn't work
  &:active {
    background-image: url("/button/icon/with-base/minimize-click.png");
  }

  &:hover {
    background-image: url("/button/icon/with-base/minimize-hover.png");
  }

  &:disabled {
    cursor: not-allowed;
    background-image: url("/button/icon/with-base/minimize-inactive.png");
  }
}
</style>
