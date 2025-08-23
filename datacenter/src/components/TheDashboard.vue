<template>
  <div class="body">

    <aside class="sidebar flex flex-col">
      <section class="flex-col">
        <p class="subtitle1 _color-secondary">Total Stores: {{ selectedData.length }}</p>
        <p class="subtitle1 _color-tertiary">United States: {{ countryCounts.US }}</p>
        <p class="subtitle1 _color-tertiary">Formosa: {{ countryCounts.FM }}</p>
        <p class="subtitle1 _color-tertiary">Singapore: {{ countryCounts.SG }}</p>
        <p class="subtitle1 _color-tertiary">Japan: {{ countryCounts.JP }}</p>
      </section>
      <section class="flex-col">
        <p class="subtitle1 _color-secondary">Latest Updated Time</p>
        <p class="subtitle1 _color-tertiary">{{ new Date().toLocaleString() }}</p>
      </section>
    </aside>

    <main class="board flex">
      <section v-if="selectedData" class="flex flex-col wrapper">
        <div class="flex-col basic-data-section">
          <Header :title="currentStore || 'No Store Selected'" />
          <div class="basic-data-container flex-row">
            <div class="left-col flex-col">
              <FormString :title="'The Name of the Store'" :value="currentStore || ''"
                @update="val => updateProperty('title', val)" />
              <div class="type-data">
                <Switch :title="'Layout'" :leftText="'food'" :rightText="'view'" />
                <Dropdown :title="'Type'" />
              </div>
              <div class="geo-data">
                <FormString :title="'Lat'" :value="selectedFeature?.geometry?.coordinates[1] || ''" />
                <FormString :title="'Lon'" :value="selectedFeature?.geometry?.coordinates[0] || ''" />
              </div>
            </div>
            <div class="right-col id-data flex-col">
              <FormString :title="'id'" :value="currentStoreId" @update="val => updateProperty('id', val)" />
              <FormString :title="'auid'" :value="currentStoreAuid" @update="val => updateProperty('auid', val)" />
              <FormString :title="'placeid'" :value="currentStorePlaceid"
                @update="val => updateProperty('placeid', val)" />
            </div>
          </div>
        </div>
        <div v-if="currentStore" class="flex-col container">
          <Header title="Detail" />
        </div>
      </section>
      <section class="file-container flex flex-col">
        <MainDropdown v-model="selectedJsonFile" :files="jsonList" @update:modelValue="handleJsonSelection" />
        <Dropdown class="" :files="storeList" :title="'Store'" @selected="handleStoreSelection" />
      </section>
    </main>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import axios from 'axios';
// Button
import MainDropdown from "./Button/MainDropdown.vue";
import Dropdown from "./Button/Dropdown.vue";
import Switch from "./Button/Switch.vue";
// Components
import FormString from "./FormString.vue";
import Header from './Nav/Header.vue';

const API = import.meta.env.VITE_DATACENTER_API;
const jsonList = ref([]);
const selectedData = ref([]);
const storeList = ref([]);
const currentStore = ref('');
const currentStoreId = ref('');
const currentStoreAuid = ref('');
const currentStorePlaceid = ref('');

const businesshour = ref([]);

// List all files
async function fetchJsonFiles() {
  try {
    const response = await axios.get(`${API}/json-files`);
    jsonList.value = response.data.map(file => file.replace(/\.json$/, ''));
  } catch (error) {
    console.error('Error fetching JSON files:', error);
  }
}
onMounted(() => {
  fetchJsonFiles();
});

// Process json data
function handleJsonSelection(file) {
  axios.get(`${API}/json-data/${file}`)
    .then(response => {
      const data = response.data;
      selectedData.value = data;

      // // 🐞 Debug console
      // console.log('features:', data);
      // console.log('selectedData.value:', selectedData.value);

      // Retrieve and list the titles of all stores
      storeList.value = data
        .map(f => (f?.properties?.title) || f?.title)
        .filter(Boolean);
      currentStore.value = '';
    })
    .catch(error => {
      console.error('Error fetching JSON data for file:', file, error);
      selectedData.value = [];
      storeList.value = [];
      currentStore.value = '';
    });
}

// Overview of the data
const countryCounts = computed(() => {
  const counts = { US: 0, FM: 0, SG: 0, JP: 0 };
  for (const item of selectedData.value) {
    const id = item.id || (item.properties && item.properties.id) || '';
    const prefix = id.split('_')[0];
    if (counts[prefix] !== undefined) {
      counts[prefix]++;
    }
  }
  return counts;
});

// Selected store
const selectedIndex = computed(() =>
  selectedData.value.findIndex(f => (f?.properties?.title || f?.title) === currentStore.value)
);

const selectedFeature = computed(() =>
  selectedIndex.value >= 0 ? selectedData.value[selectedIndex.value] : null
);

function handleStoreSelection(store) {
  currentStore.value = store;
  const idx = selectedData.value.findIndex(f =>
    (f?.properties?.title || f?.title) === store
  );

  if (idx >= 0) {
    const selectedStore = selectedData.value[idx];

    currentStoreId.value = selectedStore?.id || '?';
    currentStoreAuid.value = selectedStore?.auid || '?';
    currentStorePlaceid.value = selectedStore?.placeid || '?';
  }
}

function updateProperty(key, val) {
  const idx = selectedIndex.value;
  if (idx < 0 || !selectedFeature.value) return;

  // Ensure we have a properties object for GeoJSON format
  if (!selectedFeature.value.properties && selectedFeature.value.type === 'Feature') {
    selectedFeature.value.properties = {};
  }

  // Handle title specially to keep UI in sync
  if (key === 'title') {
    const prevTitle = selectedFeature.value.properties?.title || selectedFeature.value.title || currentStore.value || '';

    // Update both possible locations
    if (selectedFeature.value.properties) {
      selectedFeature.value.properties.title = val;
    }
    selectedFeature.value.title = val;

    currentStore.value = val;

    // Update the store list
    const listIdx = storeList.value.findIndex(t => t === prevTitle);
    if (listIdx >= 0) storeList.value.splice(listIdx, 1, val);
    return;
  }

  // For other properties, prioritize the GeoJSON structure
  if (selectedFeature.value.properties) {
    selectedFeature.value.properties[key] = val;
  } else {
    // Fallback to direct property if no properties object
    selectedFeature.value[key] = val;
  }
}
</script>

<style lang="scss" scoped>
.body {
  flex-direction: row;
  align-items: stretch;
  padding: 0px;
  width: 100vw;
  height: 100%;
  background-color: #FBFBFB;
}

.sidebar {
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.09);
  color: #000000;
  padding: 24px;
  min-width: 320px;

  justify-content: space-between;
  align-items: flex-start;
}

.board {
  flex-direction: row;
  align-items: flex-start;
  width: 928px;
  padding: 36px;
  gap: 36px
}

.container {
  gap: 12px;
}


.basic-data-section {
  gap: 12px;
}

.basic-data-container {
  gap: 24px;
}


.file-container {
  gap: 12px;
}

.nav {
  display: flex;
  width: 920px;
  justify-content: space-between;
  align-items: flex-start;
}

.dashboard-frame {
  flex-direction: column;
  align-items: flex-start;
  gap: 24px;
}

.temp-button {
  cursor: pointer;
  background-color: transparent;
  border: 0px;
  padding: 10px 16px;
  justify-content: center;
  align-items: center;
  border-radius: var(--border-button-round, 8px);
  background: var(--token-theme, #fafafa);
  color: var(--token-invert, #0e0d0f);

  font-family: Be Vietnam Pro;
  font-size: 15px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;
}

.data-section {
  max-width: 996px;
  align-items: flex-start;
  gap: 24px;
  padding: 24px;
  border-radius: 12px;
  background: #171C28;
}

.form-set {
  align-self: stretch;
  align-items: flex-start;
  gap: 24px;
}

.green {
  color: var(--1-system-green, #3DC363);
}

.wrapper {
  width: 100%;
  gap: 24px;
}

.button-set {
  align-items: flex-start;
  gap: 24px;
}

.type-data {
  gap: 24px;
}

.geo-data {
  gap: 24px;
}

.right-col {
  gap: 24px;
  width: 360px
}

.left-col {
  gap: 24px;
}
</style>