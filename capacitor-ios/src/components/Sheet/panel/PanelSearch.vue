<template>
  <section class="search-container">
    <div class="search-component">
      <TheSearch @click="search" ref="searchComponent" />
      <Close type="modal" @close="closeBottomSheet" />
    </div>
    <ListSearchTopic @click="minimizeBottomSheet" />
  </section>
</template>

<script setup>
import { ref, inject, onMounted, watch, reactive, nextTick } from 'vue';
import { Keyboard } from '@capacitor/keyboard'
import TheSearch from '../../TheSearch.vue';
import Close from '../../button/Icon/Close.vue';
import ListSearchTopic from '../../list/ListSearchTopic.vue';


const state = ref('searching')
const searchComponent = ref(null)

// Emits
const emit = defineEmits(['close', 'height-change', 'navigate']);

const search = () => {
  state.value = 'searching'
  emit('height-change', 'calc(100vh - env(safe-area-inset-top))')

  nextTick(() => {
    searchComponent.value?.focusInput()
  })
}

watch(() => state.value, (newState) => {
  switch (newState) {
    case 'searching':
      Keyboard.show()
      emit('height-change', 'calc(100vh - env(safe-area-inset-top))')

      nextTick(() => {
        searchComponent.value?.focusInput()
      })
      break
    case 'reviewing':
      Keyboard.hide()
      document.activeElement?.blur()
      break
    case 'displaying-topic':
      Keyboard.hide()
      emit('height-change', '32px')
      break
  }
}, { immediate: true })

// Buttons
const closeBottomSheet = () => {
  if (state.value === 'searching') {
    emit("close");
    Keyboard.hide()
  } else if (state.value === 'displaying-topic') {
    state.value = 'searching';
    Keyboard.show()
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