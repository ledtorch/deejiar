<template>
  <div class="thumbnail-frame flex-col">
    <div class="base">
      <p class="caption2">No.11</p>
    </div>
    <div class="base">
      <p class="caption1">title</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Button minimize card
const isVisible = ref(true);
const minimizeCard = () => {
  isVisible.value = false;
};
</script>

<style lang="scss" scoped>
.thumbnail-frame {
  min-width: 120px;
  min-height: 120px;

  padding: 4px;
  border-radius: 8px;
  background: lightgray 50%;

  justify-content: space-between;
  align-items: flex-start;

}

.minimize-button {
  position: absolute;
  top: 12px;
  right: 12px;
}

.base {
  padding: var(--Atom, 2px) var(--Unit, 4px);
  flex-direction: column;
  align-items: flex-start;
  border-radius: var(--Round-Mini, 4px);
  background: var(--Base-Invert-base, rgba(0, 0, 0, 0.60));
}
</style>