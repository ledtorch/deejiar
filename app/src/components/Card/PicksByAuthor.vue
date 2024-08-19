<template>
  <div v-if="isVisible" class="frame">
    <transition name="fade" mode="out-in">
      <div v-if="mode === 'cover'" key="cover" class="card">
        <Minimize class="minimize-button" @click="minimizeCard" />
      </div>
      <div v-else key="list" class="thumbnail-container flex-col">
        <div class="marquee-wrapper" ref="marqueeWrapper" @mousedown="handleMouseDown" @click="handleClick">
          <div class="marquee">
            <Thumbnail v-for="bar in barsList" :key="bar.properties.id" :bar="bar" @click="goToBarOnMap(bar)" />
          </div>
        </div>
        <h4>Top Bars Chosen by Deejiar </h4>
        <!-- <h4>Asia's 50 Best Bars</h4> -->
        <!-- <h4>Asia's 100 Best Bars in Taipei City</h4> -->
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Minimize from "../Button/Icon/Minimize.vue";
import Thumbnail from './Thumbnail.vue';
import barListData from '../../assets/lists/test-asias-50-best-bars.json';

const isVisible = ref(true);
const mode = ref('cover');
let intervalId = null;
const marqueeWrapper = ref(null);

const barsList = ref([]);

const fetchBarsList = async () => {
  try {
    barsList.value = barListData.features.filter(feature => feature.properties.type === "bar");
    console.log('Fetched bars:', barsList.value); // Debugging line
  } catch (error) {
    console.error('Error processing bars list:', error);
  }
};

const minimizeCard = () => {
  isVisible.value = false;
};

// 🏗️ TODO: Only render once to improve performance
const switchMode = () => {
  mode.value = mode.value === 'cover' ? 'list' : 'cover';
  clearTimeout(intervalId);
  intervalId = setTimeout(switchMode, mode.value === 'cover' ? 4000 : 8000);
};

let isScrolling = false;
let startX = 0;
let startScrollLeft = 0;

const handleMouseDown = (event) => {
  if (event.button === 0) { // Check if it's the left mouse button
    event.preventDefault();
    isScrolling = true;
    startX = event.clientX;
    startScrollLeft = marqueeWrapper.value.scrollLeft;

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  }
};

const handleMouseMove = (event) => {
  if (!isScrolling) return;
  const dx = event.clientX - startX;
  marqueeWrapper.value.scrollLeft = startScrollLeft - dx;
};

const handleMouseUp = () => {
  isScrolling = false;
  document.removeEventListener('mousemove', handleMouseMove);
  document.removeEventListener('mouseup', handleMouseUp);
};

// Prevent default click behavior if we've been scrolling
const handleClick = (event) => {
  if (isScrolling) {
    event.preventDefault();
    event.stopPropagation();
  }
};

const emit = defineEmits(['selectBar']);

const goToBarOnMap = (bar) => {
  emit('selectBar', bar);
};

onMounted(() => {
  fetchBarsList();
  intervalId = setTimeout(switchMode, 4000);
});

onUnmounted(() => {
  clearTimeout(intervalId);
  document.removeEventListener('mousemove', handleMouseMove);
  document.removeEventListener('mouseup', handleMouseUp);
});
</script>

<style lang="scss" scoped>
.frame {
  min-width: 328px;
  max-width: 100%;
  height: 204px;
  box-sizing: border-box;
  padding: 16px;
  position: relative;
}

.card,
.thumbnail-container {
  position: absolute;
  width: calc(100% - 32px);
  height: calc(100% - 32px);
  border-radius: 8px;
  border: 0.5px solid var(--silver);
  overflow: hidden;
  touch-action: pan-y;
  /* Enable vertical touch scrolling */
}

.card {
  background-image: url('../../assets/images/asia-top-50-bars.jpg');
  background-size: cover;
  background-position: top;
}

.thumbnail-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: var(--invert-primary);
  padding: 8px;
}

.marquee-wrapper {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  touch-action: pan-x;
  scroll-behavior: smooth;
  /* Enable smooth scrolling on iOS */
}

.marquee {
  flex: 1;
  gap: 12px;
  width: max-content;
}

// Hide scrollbar for Chrome, Safari and Opera
.marquee-wrapper::-webkit-scrollbar {
  display: none;
}

.marquee-wrapper {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  touch-action: pan-x;
  scroll-behavior: smooth;
  cursor: grab;
  user-select: none; // Prevent text selection during scroll
}


.marquee-wrapper:active {
  cursor: grabbing;
  /* Add this line */
}

.minimize-button {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 1;
}

// Animation
.fade-enter-active,
.fade-leave-active {
  transition: opacity 250ms ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
