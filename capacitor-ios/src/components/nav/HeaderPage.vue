<template>
  <div class="search-wrapper" :style="wrapperStyle">
    <LeftArrow @click="clickBack" />
    <p class="_title page-title">{{ pagetitle }}</p>
    <div class="right"></div>
  </div>
</template>

<script setup>
import LeftArrow from '../button/Icon/LeftArrow.vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps({
  pagetitle: { type: String, default: '' }
})

const clickBack = () => {
  router.back();
};
</script>

<style lang="scss" scoped>
.search-wrapper {
  width: 100%;
  justify-content: space-between;
  align-items: center;
}

.search-field {
  /* Fill available width from parent flex column */
  width: 100%;
  height: 36px;
  padding: 6px 8px;
  border-radius: 8px;
  background: var(--button-base);
  align-items: center;
  gap: 4px;
  transition: background 120ms ease, box-shadow 120ms ease;
}

.search-input::placeholder {
  color: var(--tertiary-text)
}

.page-title {
  color: var(--primary-text);
}

.search-wrapper {
  flex: 1 0 0;
}

.right {
  width: 24px;
  height: 24px;
}
</style>