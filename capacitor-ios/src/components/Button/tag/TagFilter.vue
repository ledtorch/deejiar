<template>
  <section class="tag-container">
    <div class="tag-title">
      <img :src="iconSrc" class="tag-icon" />
      <p class="tag-text _button-primary">{{ text }}</p>
    </div>
    <Close type="item" @close="handleClose" />
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useMapStore } from '@/stores/mapStore.js';
import Close from '../Icon/Close.vue'

const props = defineProps({
  icon: {
    type: String,
    required: true
  },
  text: {
    type: String,
    required: true
  }
})
const emit = defineEmits(['close'])

const mapStore = useMapStore();

const shouldShowFilter = computed(() => {
  console.log('currentDataSource:', mapStore.currentDataSource)
  return mapStore.currentDataSource !== 'meta'
})

const iconSrc = computed(() => {
  // Handle both full paths and icon names
  if (props.icon.startsWith('/') || props.icon.startsWith('http')) {
    return props.icon
  } else {
    // Map icon names to actual paths
    const iconMap = {
      cocktail: '/icon/collection/cocktail.png',
      icecream: '/icon/collection/icecream.png',
      taco: '/icon/collection/taco.png'
    };
    return iconMap[props.icon] || `/icon/logo/logo.png`;
  }
})

// const handleClose = async () => {
//   try {
//     await mapStore.resetToMeta();
//     emit('close');
//   } catch (error) {
//     console.error('Failed to reset to meta:', error);
//   }
// }; 

const handleClose = () => {
  mapStore.resetToMeta()
  emit('close');
  console.log('Close', mapStore.resetToMeta())
};
</script>

<style lang="scss" scoped>
.tag-container {
  cursor: pointer;

  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--unit);

  padding: var(--atom) var(--atom) var(--atom) var(--unit);
  border-radius: var(--round-m);

  width: fit-content;
  height: 32px;

  transition: all 0.2s ease;

  background: var(--primary-text);
}

.tag-title {
  display: flex;
  align-items: center;
  gap: var(--atom);
}

.tag-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.tag-text {
  color: var(--invert-primary);
}
</style>
