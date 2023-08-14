<template>
  <button
    class="icon-button"
    @click="onClick"
    :class="buttonClass"
    :style="buttonStyle"
  ></button>
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
      const baseUrl = "Button/Icon/withBase/Close_";
      let image;
      switch (this.state) {
        case "click":
          image = "Click.png";
          break;
        case "inactive":
          image = "Inactive.png";
          break;
        default:
          image = "Default.png";
          break;
      }
      return {
        backgroundImage: `url('${baseUrl}${image}')`,
      };
    },
  },
  methods: {
    onClick() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.icon-button {
  background: no-repeat center/contain;
  width: 32px;
  height: 32px;
  border: none;
  cursor: pointer;
  padding: 0;
  transition: transform 0.2s ease;
}

.icon-button.inactive {
  cursor: not-allowed;
}
</style>
