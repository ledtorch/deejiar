<template>
  <div class="bottom-sheet" :style="{ height: bottomSheetHeight }" ref="bottomSheet">
    <!-- Filter Tag - Show when collection is active -->
    <div v-if="mapStore.showTagFilter" class="filter-tag-container">
      <TagFilter :icon="tagFilterData.icon" :text="tagFilterData.text" @close="handleTagFilterClose" />
    </div>

    <!-- Drag Control Bar -->
    <div v-if="currentPanelComponent !== PanelAuth && currentPanelComponent !== PanelAuthOTP" class="control-area"
      ref="controlArea">
      <div class="control-bar"></div>
    </div>

    <!-- Dynamic Panel Content -->
    <component :is="currentPanelComponent" v-bind="panelProps" @close="handlePanelClose"
      @height-change="updateSheetHeight" @navigate="handleNavigation" @show-tag-filter="handleShowTagFilter" />
  </div>
</template>

<script setup>
import { ref, computed, watch, provide } from 'vue';
import { useRouter } from 'vue-router';
import { useMapStore } from '@/stores/mapStore.js';

// Import all panels
import PanelDefault from './panel/PanelDefault.vue';
import PanelAuth from './panel/PanelAuth.vue';
import PanelAuthOTP from './panel/PanelAuthOTP.vue';
import PanelSearch from './panel/PanelSearch.vue';
import PanelStore from './panel/PanelStore.vue';

import TagFilter from './../button/tag/TagFilter.vue'

const router = useRouter();
const mapStore = useMapStore();

// Props from Map.vue
const props = defineProps({
  store: Object,
  initialPanel: {
    type: String,
    default: 'default'
  }
});

// Emits
const emit = defineEmits(['reset', 'panel-change']);

// Sheet height management
const bottomSheetHeight = ref('60px');
const bottomSheet = ref(null);
const controlArea = ref(null);

// Panel state management
const currentPanel = ref(props.initialPanel);
const panelData = ref({});
const panelComponents = {
  default: PanelDefault,
  auth: PanelAuth,
  authOTP: PanelAuthOTP,
  store: PanelStore,
  search: PanelSearch
};

// Default panel
const currentPanelComponent = computed(() => {
  return panelComponents[currentPanel.value] || PanelDefault;
});

const panelProps = computed(() => {
  // Store panel data
  if (currentPanel.value === 'store' && props.store) {
    return { store: props.store };
  }

  // Auth panel data
  if (currentPanel.value === 'authOTP' && panelData.value.email) {
    return {
      email: panelData.value.email,
      action: panelData.value.action || 'register'
    };
  }

  return {};
});

// ===========================
// TagFilter State & Handlers
// ===========================
const tagFilterData = computed(() => {
  const collectionTags = {
    cocktail: { icon: '/icon/collection/cocktail.png', text: 'Best Bars After Dark — Taipei' },
    icecream: { icon: '/icon/collection/icecream.png', text: 'Ice Cream for a Rainy Day' },
    taco: { icon: '/icon/collection/taco.png', text: 'Tacos in the Alley' }
  }
  return collectionTags[mapStore.activeCollectionType] || { icon: '', text: '' }
})

const handleTagFilterClose = () => {
  mapStore.resetToMeta()
}

// Height presets
const HEIGHTS = {
  MIN: '32px',
  DEFAULT: '476px',
  AUTH: '290px',
  STORE: '467px',
  FULL: `calc(100vh - env(safe-area-inset-top))`,
};

// Watch for store selection from Map.vue
watch(() => props.store, (newStore) => {
  if (newStore) {
    currentPanel.value = 'store';
    bottomSheetHeight.value = HEIGHTS.STORE;
  } else {
    currentPanel.value = 'default';
    bottomSheetHeight.value = HEIGHTS.DEFAULT;
  }
});

// Panel management methods
const switchPanel = (panelName, data = null) => {
  currentPanel.value = panelName;

  // Pass data to panel, skip if null
  if (data) {
    Object.assign(panelData.value, data);
  }

  // Set panel height
  switch (panelName) {
    case 'store':
      bottomSheetHeight.value = HEIGHTS.STORE;
      break;
    case 'auth':
      bottomSheetHeight.value = HEIGHTS.AUTH;
      break;
    case 'authOTP':
      bottomSheetHeight.value = HEIGHTS.FULL;
      break;
    case 'search':
      bottomSheetHeight.value = HEIGHTS.FULL;
      break;
    default:
      bottomSheetHeight.value = HEIGHTS.DEFAULT;
  }

  emit('panel-change', panelName);
};

// Handle panel events
const handlePanelClose = () => {
  if (currentPanel.value === 'store') {
    emit('reset'); // Tell Map.vue to remove marker
  }

  currentPanel.value = 'default';
  bottomSheetHeight.value = HEIGHTS.MIN;
};

const updateSheetHeight = (height) => {
  bottomSheetHeight.value = height;
};

const handleNavigation = (route) => {
  router.push(route);
};

// Dragging functionality
const isDragging = ref(false);
let startY = 0;
let startHeight = 0;

const dragStart = (event) => {
  event.preventDefault();
  isDragging.value = true;
  startY = event.pageY || event.touches?.[0].pageY;
  startHeight = parseInt(bottomSheetHeight.value);
  bottomSheet.value.classList.add('dragging');

  document.addEventListener('mousemove', dragging);
  document.addEventListener('mouseup', dragStop);
  document.addEventListener('touchmove', dragging, { passive: false });
  document.addEventListener('touchend', dragStop);
};

const dragging = (event) => {
  if (!isDragging.value) return;

  event.preventDefault();
  const currentY = event.pageY || event.touches?.[0].pageY;
  const delta = startY - currentY;
  const newHeight = Math.max(32, Math.min(window.innerHeight, startHeight + delta));

  bottomSheetHeight.value = `${newHeight}px`;
};

const dragStop = () => {
  isDragging.value = false;
  bottomSheet.value.classList.remove('dragging');

  const currentHeight = parseInt(bottomSheetHeight.value);

  // Snap to nearest preset height
  if (currentHeight < 100) {
    bottomSheetHeight.value = HEIGHTS.MIN;
  } else if (currentHeight > 600 && currentPanel.value === 'store' && props.store) {
    // Navigate to detail view if dragged high enough
    router.push({
      name: 'detail',
      params: { id: props.store.id }
    });
  } else if (currentHeight > 500) {
    bottomSheetHeight.value = HEIGHTS.FULL;
  } else {
    // Return to panel's default height
    const defaultHeight = HEIGHTS[currentPanel.value.toUpperCase()] || HEIGHTS.DEFAULT;
    bottomSheetHeight.value = defaultHeight;
  }

  document.removeEventListener('mousemove', dragging);
  document.removeEventListener('touchmove', dragging);
  document.removeEventListener('mouseup', dragStop);
  document.removeEventListener('touchend', dragStop);
};

// Setup drag listeners
watch(controlArea, (el) => {
  if (el) {
    el.addEventListener('mousedown', dragStart);
    el.addEventListener('touchstart', dragStart, { passive: false });
  }
}, { immediate: true });

// Expose methods for parent component
defineExpose({
  switchPanel,
  updateSheetHeight
});

provide('bottomSheetControls', {
  switchPanel,
  updateSheetHeight,
  getCurrentPanel: () => currentPanel.value,
  closePanel: handlePanelClose
});
</script>

<style lang="scss" scoped>
.bottom-sheet {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 32px;
  max-height: 100vh;
  padding: 0;
  border-radius: var(--round-xl) var(--round-xl) 0 0;
  background-color: var(--base);
  transition: height 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;

  &.dragging {
    transition: none;
  }
}

.control-area {
  cursor: grab;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 32px;
  padding: 12px 0;
  touch-action: none;
  flex-shrink: 0;

  &:active {
    cursor: grabbing;
  }
}

.control-bar {
  width: 48px;
  height: 4px;
  border-radius: 4px;
  background-color: #808cab;
}

.filter-tag-container {
  position: fixed;
  top: calc(var(--wrapper) + env(safe-area-inset-top));
  left: 0;
  right: 0;
  z-index: 2;

  display: flex;
  justify-content: center;
  padding: var(--block) 0 0 0;
}
</style>