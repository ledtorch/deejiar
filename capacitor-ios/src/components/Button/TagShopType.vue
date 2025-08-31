<template>
  <div class="tag-shop-frame">
    <div class="icon-image" :style="icon"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  store: {
    type: Object,
    default: () => ({}),
  },
});

const icon = computed(() => {
  const type = props.store?.type;
  const path = `/icon/category/${type}.png`;
  console.log("🆗 Component -> TagShopType, Icon Path: " + path);
  return { backgroundImage: `url('${path}')` };
});

</script>

<style lang="scss" scoped>
.tag-shop-frame {
  align-items: center;
  width: 32px;
  height: 32px;
  padding: var(--quark);
  border-radius: var(--round-m);
  background: var(--primary-text);
}

.icon-image {
  width: 28px;
  height: 28px;
  background: no-repeat center/cover;
}
</style>
