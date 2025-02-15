<template>
  <div class="tag-shop-frame">
    <div class="icon-image" :style="icon"></div>
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
      const type = this.store?.type;
      const path = `/icon/category/${type}.png`;

      // // 🐞 Debug console
      // console.log("🆗 Component -> TagShopType, Icon Path: " + path);
      return { backgroundImage: `url('${path}')` };
    },
  },
};
</script>

<style lang="scss" scoped>
h2 {
  color: black;
}

.tag-shop-frame {
  align-items: center;
  gap: 4px;
  padding: 2px;
  width: 32px;
  height: 32px;
  border-radius: var(--border-button-round, 8px);
  background: var(--token-theme, #fafafa);
}

.icon-image {
  width: 28px;
  height: 28px;
  background: no-repeat center/cover;
}
</style>
