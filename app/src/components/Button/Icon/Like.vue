<template>
  <button class="icon-button" @click="onClick" :class="buttonClass" :style="buttonStyle"></button>
</template>

<script>
export default {
  props: {
    state: {
      type: String,
      default: "default",
    },
  },
  computed: {
    buttonClass() {
      return this.state === "inactive" ? "inactive" : "";
    },
    buttonStyle() {
      let imageFileName;
      switch (this.state) {
        case "click":
          imageFileName = "click.png";
          break;
        case "inactive":
          imageFileName = "inactive.png";
          break;
        default:
          imageFileName = "default.png";
          break;
      }
      return {
        backgroundImage: this.backgroundImageUrl(imageFileName),
      };
    },
    methods: {
      backgroundImageUrl(imageFileName) {
        const baseUrl = `${window.location.protocol}//${window.location.host}`;
        return `url('${baseUrl}/button/icon/with-base/like-${imageFileName}')`;
      },
    },
    onClick() {
      this.$emit("like");
    },
  },
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
  transition: transform 0.2s ease;
}

.icon-button.inactive {
  cursor: not-allowed;
}
</style>
