<template>
  <div class="tag-shop-frame">
    <div class="icon-image" :style="icon"></div>
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
    icon() {
      const type = this.store?.type; // Set Taco as default png to prevent the undefined msg
      const path = `/Icon/category/${type}.png`;
      console.log("🆗 Component -> TagShopType, Icon Path: " + path);
      return { backgroundImage: `url('${path}')` };
    },
  },
};
</script>

<style scoped>
.tag-shop-frame {
  align-items: center;
  gap: 4px;
}

.icon-image {
  background: no-repeat center/cover;
  width: 24px;
  height: 24px;
}
</style>
