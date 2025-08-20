<template>
  <div class="container">
    <h4 class="_color-primary">{{ title }}</h4>
    <Primary label="Update" />
  </div>
</template>

<script setup>
const props = defineProps({
  title: { type: String, default: '' },
})
import Primary from "../Button/Primary.vue";
</script>

<style lang="scss" scoped>
.container {
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}
</style>
