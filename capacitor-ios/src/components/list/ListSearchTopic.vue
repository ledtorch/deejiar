<template>
  <button class="list-container" @click="navigateToTaipei">
    <div class="topic-header">

      <img src="@/assets/images/taipei.jpg" class="topic-icon">
      <p class="topic-title _title">Start from Taipei City</p>
    </div>

    <img :src="pinPoint" class="topic-button-icon" />
  </button>
</template>

<script setup>
import { useMapStore } from '@/stores/mapStore.js';
import pinPoint from '@/assets/buttons/pin-point.svg';

const mapStore = useMapStore();

const navigateToTaipei = () => {
  const TAIPEI_COORDINATES = [121.55750335591597, 25.041676750617142]

  // Directly assign to the ref object
  mapStore.navigateToLocation.value = {
    coordinates: TAIPEI_COORDINATES,
    zoomLevel: 13.5
  }
}
</script>


<style lang="scss" scoped>
.list-container {
  display: flex;
  width: 100%;
  padding: var(--atom);
  justify-content: space-between;
  align-items: center;
  border-radius: var(--round-m);
  background-color: var(--gray-button);

  &:active {
    opacity: 0.7;
  }
}

.topic-header {
  align-items: center;
  gap: var(--unit);
}

.topic-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--round-s);
}

.topic-button-icon {
  width: 24px;
  height: 24px;
}

.topic-title {
  color: var(--primary-text);
}
</style>