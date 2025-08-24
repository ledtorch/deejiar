<template>
  <div class="header-container">
    <h4 class="_color-primary">{{ title }}</h4>
    <PrimaryButton :label="loading ? 'Saving...' : 'Update'" @click="handleUpdate" :disabled="loading" />
  </div>
</template>

<script setup>
import PrimaryButton from "../Button/Primary.vue";
import { ref } from 'vue';

const props = defineProps({
  title: { type: String, default: '' },
});

const emit = defineEmits(['update']);

const loading = ref(false);

function handleUpdate() {
  if (!loading.value) {
    loading.value = true;
    emit('update');
    // Reset loading state after parent handles it
    setTimeout(() => {
      loading.value = false;
    }, 2000);
  }
}
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
