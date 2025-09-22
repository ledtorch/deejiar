<template>
  <button class="list-container" @click="navigateToStore">
    <img :src="storeIcon" class="store-icon">
    <div>
      <p class="store-name _title">{{ storeData.title }}</p>
      <p class="store-text _body1">&nbsp;·&nbsp;{{ storeData.type }}</p>
    </div>
  </button>
</template>

<script setup>
import { computed } from 'vue';
import { useMapStore } from '@/stores/mapStore.js';
const mapStore = useMapStore();

const props = defineProps({
  storeData: {
    type: Object,
    required: true
  }
})

const storeIcon = computed(() => {
  const type = props.storeData.type
  return new URL(`../../assets/icons/types/${type}.png`, import.meta.url).href
})

const navigateToStore = () => {
  console.log('🔍 Search result clicked:', props.storeData.title)

  // Use centralized store selection - data is already in correct format
  mapStore.selectStore(props.storeData, true)

  // Emit event to parent (PanelSearch) to handle UI state
  emit('store-selected', props.storeData)
}

const emit = defineEmits(['store-selected'])
</script>


<style lang="scss" scoped>
.list-container {
  display: flex;
  align-items: center;
  gap: var(--unit);

  &:active {
    opacity: 0.7;
  }
}

.store-icon {
  width: 28px;
  height: 28px;
}

.store-name {
  color: var(--primary-text);
}

.store-text {
  color: var(--secondary-text);
}
</style>