<template>
  <button class="icon-button" @click="onClick"></button>
</template>

<script setup>
const emit = defineEmits(['close']);

const onClick = () => {
  emit('close');
};
</script>

<style lang="scss" scoped>
.icon-button {
  cursor: pointer;
  min-width: 32px;
  min-height: 32px;
  background: no-repeat center/contain;
  background-image: url("/button/icon/with-base/close-default.png");
}
</style>
