<template>
  <div class="frame">
    <div class="image" :style="frame"></div>
    <h2>{{ store ? store.type : "" }}</h2>
  </div>
</template>

<script>
export default {
  props: {
    store: {
      type: Object,
      default: () => ({}),
    },
  },

  computed: {
    frame() {
      const type = this.store?.type || "Taco"; // Set Taco as default png to prevent the undefined msg
      const path = `/Icon/category/${type}.png`;
      console.log("🆗 Component -> TagShopType, Icon Path: " + path);
      return `background: url('${path}') center/cover no-repeat; width: 24px; height: 24px;`;
    },
  },
};
</script>

<style scoped>
.frame {
  display: inline-flex;
  flex-direction: row;
  align-items: center;
  gap: 4px;
}
</style>
