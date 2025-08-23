<template>
  <div class="header-container">
    <h4 class="_color-primary">{{ title }}</h4>
    <PrimaryButton label="Update" />
  </div>
</template>

<script setup>
const props = defineProps({
  title: { type: String, default: '' },
})
import PrimaryButton from "../Button/Primary.vue";
</script>

<style lang="scss" scoped>
.header-container {
  justify-content: space-between;
  height: auto;
  width: 100%;
  align-items: center;
  align-self: stretch;
}
</style>
