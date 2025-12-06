<template>
  <main class="page">

    <aside class="sidebar">
      <section class="section-container">
        <p class="title _color-secondary">Total Stores: {{ featureCollection?.features?.length || 0 }}</p>
        <p class="title _color-tertiary">United States: {{ countryCounts.US }}</p>
        <p class="title _color-tertiary">Formosa: {{ countryCounts.FM }}</p>
        <p class="title _color-tertiary">Singapore: {{ countryCounts.SG }}</p>
        <p class="title _color-tertiary">Japan: {{ countryCounts.JP }}</p>
      </section>
      <section class="section-container">
        <p class="title _color-secondary">Latest Updated Time</p>
        <p class="title _color-tertiary">{{ new Date().toLocaleString() }}</p>
      </section>
    </aside>

    <div class="board flex">
      <section class="section-container wrapper">
        <div class="basic-data-section">
          <Header :title="currentStore || 'No Store Selected'" @update="saveChanges" />
          <div class="basic-data-container">
            <div class="left-col">
              <FormString :title="'The Name of the Store'" :value="currentStore || ''"
                @update="val => updateProperty('title', val)" />
              <div class="type-data">
                <Switch :title="'Layout'" :leftText="'food'" :rightText="'view'"
                  :value="selectedFeature?.properties?.layout" @update="val => updateProperty('layout', val)" />
                <Dropdown :title="'Type'" :value="selectedFeature?.properties?.type"
                  :options="['restaurant', 'museum', 'shop', 'cafe', 'landmark']"
                  @update="val => updateProperty('type', val)" />
              </div>
              <div class="geo-data">
                <FormString :title="'Lat'" :value="selectedFeature?.geometry?.coordinates[1]?.toString() || ''"
                  @update="val => updateCoordinate('lat', val)" />
                <FormString :title="'Lon'" :value="selectedFeature?.geometry?.coordinates[0]?.toString() || ''"
                  @update="val => updateCoordinate('lon', val)" />
              </div>
            </div>
            <div class="right-col id-data flex-col">
              <FormString :title="'id'" :value="selectedFeature?.properties?.id || ''"
                @update="val => updateProperty('id', val)" />
              <FormString :title="'auid'" :value="selectedFeature?.properties?.auid || ''"
                @update="val => updateProperty('auid', val)" />
              <FormString :title="'placeid'" :value="selectedFeature?.properties?.placeid || ''"
                @update="val => updateProperty('placeid', val)" />
            </div>
          </div>
        </div>
        <div v-if="currentStore" class="container">
          <Header title="Detail" />
        </div>
      </section>
      <section class="file-container">
        <MainDropdown v-model="selectedJsonFile" :options="jsonList" @update:modelValue="handleJsonSelection" />
        <Dropdown :title="'Store'" :options="storeList" @selected="selectStore" />
      </section>
    </div>

  </main>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import axios from 'axios';
// Button
import MainDropdown from "../components/buttons/MainDropdown.vue";
import Dropdown from "../components/buttons/Dropdown.vue";
import Switch from "../components/buttons/Switch.vue";
// Components
import Header from '../components/navs/Header.vue';
import FormString from "../components/forms/FormString.vue";

const API = import.meta.env.VITE_DATACENTER_API;

// Data
const jsonList = ref([]);
const selectedJsonFile = ref('');
const featureCollection = ref(null);
const originalData = ref(null);

const storeList = ref([]);
const currentStore = ref('');

// 🏗️🏗️🏗️
const hasChanges = ref(false);
const saveMessage = ref('');
const saveError = ref(false);

// List all files
async function fetchJsonFiles() {
  try {
    const response = await axios.get(`${API}/admin/auth/json-files`);
    jsonList.value = response.data.map(file => file.replace(/\.json$/, ''));
  } catch (error) {
    console.error('Error fetching JSON files:', error);
  }
}

onMounted(() => {
  fetchJsonFiles();
});

// Process json data
async function handleJsonSelection(file) {
  try {
    selectedJsonFile.value = file;
    const response = await axios.get(`${API}/json-data/${file}`);
    const data = response.data;

    // Store working copy and original for change tracking
    featureCollection.value = data;
    originalData.value = JSON.parse(JSON.stringify(data)); // ❓ Deep copy
    hasChanges.value = false;
    saveMessage.value = '';

    // Retrieve and list the titles of all stores
    if (data?.features) {
      storeList.value = data.features
        .map(f => (f?.properties?.title) || f?.title)
        .filter(Boolean);
    } else {
      storeList.value = [];
    }

    currentStore.value = '';
  } catch (error) {
    console.error('Error fetching JSON data for file:', file, error);
    featureCollection.value = null;
    originalData.value = null;
    storeList.value = [];
    currentStore.value = '';
  }
}

// Overview of the data
const countryCounts = computed(() => {
  const counts = { US: 0, FM: 0, SG: 0, JP: 0 };
  if (!featureCollection.value?.features) return counts;

  for (const feature of featureCollection.value.features) {
    const id = feature?.properties?.id || '';
    const prefix = id.split('_')[0];
    if (counts[prefix] !== undefined) {
      counts[prefix]++;
    }
  }
  return counts;
});

// Selected store
const selectedIndex = computed(() => {
  if (!featureCollection.value?.features || !currentStore.value) return -1;
  return featureCollection.value.features.findIndex(
    f => f?.properties?.title === currentStore.value
  );
});

const selectedFeature = computed(() => {
  if (selectedIndex.value >= 0 && featureCollection.value?.features) {
    return featureCollection.value.features[selectedIndex.value];
  }
  return null;
});

function selectStore(store) {
  currentStore.value = store;
}

// Edit functions
function updateCoordinate(type, val) {
  if (!selectedFeature.value) return;

  const numVal = parseFloat(val);
  if (isNaN(numVal)) return;

  // Ensure geometry exists
  if (!selectedFeature.value.geometry) {
    selectedFeature.value.geometry = { type: 'Point', coordinates: [0, 0] };
  }

  if (type === 'lon') {
    selectedFeature.value.geometry.coordinates[0] = numVal;
  } else if (type === 'lat') {
    selectedFeature.value.geometry.coordinates[1] = numVal;
  }

  checkForChanges();
}

// Add change detection
function checkForChanges() {
  hasChanges.value = JSON.stringify(featureCollection.value) !== JSON.stringify(originalData.value);
}

// Add save function
async function saveChanges() {
  if (!selectedJsonFile.value || !featureCollection.value) {
    console.error('No file selected or no data to save');
    return;
  }

  try {
    saveMessage.value = 'Saving...';
    saveError.value = false;

    const response = await axios.post(
      `${API}/save/${selectedJsonFile.value}`,
      featureCollection.value
    );

    saveMessage.value = `Saved successfully as ${response.data.filename}`;
    saveError.value = false;

    // Update the original data to match saved state
    originalData.value = JSON.parse(JSON.stringify(featureCollection.value));
    hasChanges.value = false;

    // Update the selected file to the new filename (without extension)
    const newFilename = response.data.filename.replace(/\.json$/, '');
    selectedJsonFile.value = newFilename;

    // Refresh the file list
    await fetchJsonFiles();

    // Show success message
    alert(`File saved successfully as ${response.data.filename}`);

    // Clear message after 3 seconds
    setTimeout(() => {
      saveMessage.value = '';
    }, 3000);
  } catch (error) {
    console.error('Error saving changes:', error);
    saveMessage.value = error.response?.data?.detail || 'Error saving changes';
    saveError.value = true;
    alert('Error saving changes: ' + (error.response?.data?.detail || error.message));
  }
}

// Update the updateProperty function to include change detection
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
  } else {
    // For other properties, prioritize the GeoJSON structure
    if (selectedFeature.value.properties) {
      selectedFeature.value.properties[key] = val;
    } else {
      // Fallback to direct property if no properties object
      selectedFeature.value[key] = val;
    }
  }

  // Check for changes after any update
  checkForChanges();
}

// // 🐞 Debug console
// watch(selectedFeature, (newVal) => {
//   console.log('selectedFeature changed:', newVal);
//   if (newVal) {
//     console.log('Properties:', newVal.properties);
//     console.log('Layout:', newVal.properties?.layout);
//   }
// });

</script>

<style lang="scss" scoped>
.page {
  display: flex;
  align-items: stretch;
  padding: 0px;
  width: 100vw;
  height: 100%;
  background-color: #FBFBFB;
}

.sidebar {
  display: flex;
  flex-direction: column;
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

.section-container {
  display: flex;
  flex-direction: column;
}


.basic-data-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.basic-data-container {
  gap: 24px;
}


.file-container {
  display: flex;
  flex-direction: column;
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
  flex-direction: column;
  gap: 24px;
}
</style>