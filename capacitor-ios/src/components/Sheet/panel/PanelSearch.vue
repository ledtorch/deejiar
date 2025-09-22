<template>
  <section class="search-container">
    <div class="search-component">
      <TheSearch @click="search" ref="searchComponent" @submit="performSearch" />
      <Close type="modal" @close="closeBottomSheet" />
    </div>
    <ListSearchTopic v-if="searchResults.length === 0" @click="minimizeBottomSheet" />


    <div v-if="searchResults.length > 0" class="results-container">
      <ListSearchResult v-for="store in searchResults" :key="store.id" :storeData="store" />
    </div>

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
import ListSearchResult from '../../list/ListSearchResult.vue';

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
    console.log(`📊 Found ${data.count} results out of ${data.total} total stores`);

    // Store the formatted results for rendering
    searchResults.value = data.results || [];

    console.log('🔍 Search results stored:', searchResults.value);

  } catch (error) {
    console.error('❌ Search failed:', error);
    searchResults.value = []; // Clear results on error
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

.results-container {
  flex-direction: column;
  gap: var(--block);
  padding: var(--division) 0 0 0;
}
</style>