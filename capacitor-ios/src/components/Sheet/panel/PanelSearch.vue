<template>
  <section class="search-container">
    <div class="search-component">
      <TheSearch />
      <Close type="modal" @close="closeBottomSheet" />
    </div>
    <ListSearchTopic @click="minimizeBottomSheet" />
  </section>
</template>

<script setup>
import TheSearch from '../../TheSearch.vue';
import Close from '../../button/Icon/Close.vue';
import ListSearchTopic from '../../list/ListSearchTopic.vue';
import { ref, defineEmits } from 'vue';

const state = ref('default');

// Emits
const emit = defineEmits(['close', 'height-change', 'navigate']);

// Buttons
const closeBottomSheet = () => {
  if (state.value === 'default') {
    emit("close");
  } else if (state.value === 'displaying-topic') {
    state.value = 'default';
    emit('height-change', 'calc(100vh - env(safe-area-inset-top))');
  }
};

// Minimize bottom sheet to 32px (HEIGHTS.MIN defined in parent BottomSheet.vue)
const minimizeBottomSheet = () => {
  state.value = 'displaying-topic';
  emit('height-change', '32px');
};
</script>

<style lang="scss" scoped>
.search-container {
  display: flex;
  flex-direction: column;
  padding: 0 var(--wrapper);
  gap: var(--division);
}

.search-component {
  justify-content: space-between;
  gap: var(--block);
}

.collection-container {
  flex-direction: column;
  gap: var(--box);
  padding: var(--block) 0 var(--wrapper) 0;
}

.collection-title {
  color: var(--tertiary-text);
}
</style>