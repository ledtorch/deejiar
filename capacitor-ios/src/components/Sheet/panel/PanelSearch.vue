<template>
  <section class="search-container">
    <div class="search-component">
      <TheSearch @click="search" ref="searchComponent" @submit="performSearch" />
      <Close type="modal" @close="closeBottomSheet" />
    </div>
    <ListSearchTopic @click="minimizeBottomSheet" />

    <!-- Search Results -->
    <!-- <div v-else-if="searchResults.length > 0" class="results-container">
      <p class="results-count _caption1">{{ searchResults.length }} results found</p>
      <div class="results-list">
        <ListSearchResult v-for="store in searchResults" :key="store.id" :storeData="store"
          @click="handleStoreSelect(store)" />
      </div>../../form/TheSearch.vue
    </div> -->

    <!-- No Results -->
    <!-- <div v-else-if="hasSearched && searchResults.length === 0" class="no-results">
      <p class="_body1">No stores found for "{{ lastSearchQuery }}"</p>
      <p class="_caption1">Try a different search term</p>
    </div> -->

  </section>
</template>

<script setup>
import { ref, inject, onMounted, watch, reactive, nextTick } from 'vue';
import { Keyboard } from '@capacitor/keyboard'
import { useMapStore } from '@/stores/mapStore.js';
import TheSearch from '../../form/TheSearch.vue';
import Close from '../../button/Icon/Close.vue';
import ListSearchTopic from '../../list/ListSearchTopic.vue';

// Stores
const mapStore = useMapStore();

// State
const state = ref('searching')
const searchComponent = ref(null)
const searchResults = ref([]);

// Emits
const emit = defineEmits(['close', 'height-change', 'navigate']);

const search = () => {
  state.value = 'searching'
  emit('height-change', 'calc(100vh - env(safe-area-inset-top))')
}

// Perform search
const performSearch = async (query = '') => {
  console.log('🔍 performSearch called with query:', query);

  const trimmedQuery = query.trim();

  // For now, we'll just test with the query - no type filtering yet
  if (!trimmedQuery) {
    console.log('No search query provided');
    return;
  }

  console.log('🔍 Starting search for:', trimmedQuery);

  try {
    // Build query parameters
    const params = new URLSearchParams();
    params.append('q', trimmedQuery);

    // Construct API URL
    const apiUrl = `${import.meta.env.VITE_API_URL}/api/search?${params}`;
    console.log('📡 API URL:', apiUrl);

    // Call search API
    const response = await fetch(apiUrl);

    if (!response.ok) {
      throw new Error(`Search failed: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    // Log the raw API response
    console.log('✅ Raw API Response:', data);

    // Log specific details about the results
    console.log(`📊 Found ${data.count} results out of ${data.total} total stores`);

    if (data.results && data.results.length > 0) {
      console.log('🏪 First few results:');
      data.results.slice(0, 3).forEach((feature, index) => {
        console.log(`  ${index + 1}. ${feature.properties.title} (${feature.properties.type})`);
        console.log(`     Coordinates: [${feature.geometry.coordinates[0]}, ${feature.geometry.coordinates[1]}]`);
        console.log(`     Tags: ${feature.properties.storetag?.join(', ') || 'none'}`);
      });
    } else {
      console.log('❌ No results found');
    }

    // Log search filters used
    console.log('🔧 Search filters:', data.filters);

  } catch (error) {
    console.error('❌ Search failed:', error);
    console.error('Error details:', {
      message: error.message,
      stack: error.stack
    });
  }
};

watch(() => state.value, (newState) => {
  switch (newState) {
    case 'searching':
      Keyboard.show()
      emit('height-change', 'calc(100vh - env(safe-area-inset-top))')
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