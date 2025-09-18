<template>
  <button class="list-container" @click="navigateToStore">
    <img :src="storeData.icon" class="store-icon">
    <div>
      <p class="store-name _title">{{ storeData.title }} Test</p>
      <p class="store-text _body1">· {{ storeData.subtitle }} TestTest</p>
    </div>
  </button>
</template>

<script setup>
import { useMapStore } from '@/stores/mapStore.js';
const mapStore = useMapStore();

const props = defineProps({
  storeData: {
    type: Object,
    required: true
  }
})

const navigateToStore = () => {
  const store_coordinates = [props.storeData.longitude, props.storeData.latitude]

  mapStore.navigateToLocation.value = {
    coordinates: store_coordinates,
    zoomLevel: 13.5
  }
}
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
  width: 32px;
  height: 32px;
}

.store-name {
  color: var(--primary-text);
}

.store-text {
  color: var(--secondary-text);
}
</style>