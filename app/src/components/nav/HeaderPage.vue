<template>
  <div class="header-container" :style="wrapperStyle">
    <LeftArrow @click="clickBack" />
    <h5 class="page-title">{{ pagetitle }}</h5>
    <div class="right"></div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import LeftArrow from '../button/Icon/LeftArrow.vue';

const router = useRouter();

const props = defineProps({
  pagetitle: { type: String, default: '' }
})

const clickBack = () => {
  router.back();
};
</script>

<style lang="scss" scoped>
.header-container {
  width: 100%;
  justify-content: space-between;
  align-items: center;

  background-color: var(--background);
}

.page-title {
  color: var(--primary-text);
}

.right {
  width: 24px;
  height: 24px;
}
</style>