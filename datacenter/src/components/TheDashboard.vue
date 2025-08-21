<template>
  <div class="body">

    <section class="sidebar flex flex-col">
      <div class="flex-col">
        <p class="subtitle1 _color-secondary">Total Stores: {{ selectedData.length }}</p>
        <p class="subtitle1 _color-tertiary">United States: {{ countryCounts.US }}</p>
        <p class="subtitle1 _color-tertiary">Formosa: {{ countryCounts.FM }}</p>
        <p class="subtitle1 _color-tertiary">Singapore: {{ countryCounts.SG }}</p>
        <p class="subtitle1 _color-tertiary">Japan: {{ countryCounts.JP }}</p>
      </div>
      <div class="flex-col">
        <p class="subtitle1 _color-secondary">Latest Updated Time</p>
        <p class="subtitle1 _color-tertiary">{{ new Date().toLocaleString() }}</p>
      </div>
    </section>

    <section class="board flex">
      <div v-if="selectedData" class="flex flex-col wrapper">
        <div class="flex-col container">
          <Header :title="currentFile || 'No File Selected'" />
          <Switch />
        </div>
        <div class="flex-col container">
          <Header title="Store" />
        </div>
      </div>
      <Dropdown class="" :files="jsonList" :label="'json'" :placeholder="'No file selected'"
        @selected="handleJsonSelection" />
      <Dropdown class="" :files="storeList" :label="'store'" :placeholder="'No store loaded'"
        @selected="handleStoreSelection" />
    </section>


  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import axios from 'axios';
// Button
import Dropdown from "./Button/Dropdown.vue";
import Switch from "./Button/Switch.vue";
import RightArrow from "./Button/RightArrow.vue";
import LeftArrow from "./Button/LeftArrow.vue";
// Components
import FormString from "./FormString.vue";
import FormStringNest from "./FormStringNest.vue";
import FormBusinessHour from "./FormBusinessHour.vue";
import Header from './Nav/Header.vue';

const API = import.meta.env.VITE_DATACENTER_API;
const jsonList = ref([]);
const selectedData = ref([]);
const currentFile = ref('');
const storeList = ref([]);
const currentStore = ref('');
const basicProperties = [
  'id', 'title', 'type', 'layout', 'icon', 'description', 'storefront-day', 'storefront-night'
];
const geoProperties = [
  'address', 'latitude', 'longitude', 'auid', 'placeid'
];
const timeProperties = ref([]);
const products = ['item1', 'item2', 'item3', 'item4', 'item5'];
const productProperties = ['name', 'description', 'image', 'price'];
const currentPage = ref(1);
const featuresPerPage = ref(10);

const totalPages = computed(() =>
  Math.ceil(selectedData.value.length / featuresPerPage.value)
);
const paginatedFeatures = computed(() => {
  const start = (currentPage.value - 1) * featuresPerPage.value;
  const end = start + featuresPerPage.value;
  return selectedData.value.slice(start, end);
});
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

async function fetchJsonList() {
  try {
    const response = await axios.get(`${API}/json-files`);
    jsonList.value = response.data.map(file => file.replace(/\.json$/, ''));
  } catch (error) {
    console.error('Error fetching JSON files:', error);
  }
}

function handleJsonSelection(file) {
  axios.get(`${API}/json-data/${file}`)
    .then(response => {
      // 🐞 Debug console
      const data = response.data;
      // Normalize: use FeatureCollection.features if present; else assume array
      const features = Array.isArray(data?.features) ? data.features : Array.isArray(data) ? data : [];
      selectedData.value = features;
      currentFile.value = file;
      // Build store list from properties.title when available
      storeList.value = features
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

function handleStoreSelection(store) {
  currentStore.value = store;
}

function updateFeature(featureId, [prop, value]) {
  let feature = selectedData.value.find(f => f.id === featureId);
  if (feature) {
    feature[prop] = value;
  }
}

function updateNestedObj(featureId, product, [prop, value]) {
  let feature = selectedData.value.find(f => f.id === featureId);
  if (feature && feature[product]) {
    feature[product][prop] = value;
  }
}

function updateBusinessHour(featureId, newBusinessHour) {
  let feature = selectedData.value.find(f => f.id === featureId);
  if (feature) {
    feature.businesshour = newBusinessHour;
  }
}

function addNewFeature() {
  if (selectedData.value.length === 0) {
    console.warn('No features available to duplicate.');
    return;
  }
  // Clone the latest feature
  const latestFeature = selectedData.value[selectedData.value.length - 1];
  const newFeature = JSON.parse(JSON.stringify(latestFeature));
  // Generate a new unique ID for the new feature
  newFeature.id = selectedData.value.length + 1;
  // Add the new feature to the selectedData array
  selectedData.value.push(newFeature);
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
}
function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
}

async function updateJSON() {
  try {
    const filename = currentFile.value;
    const response = await axios.post(`${API}/save/${filename}`, selectedData.value);
    // 🐞 Debug console
    console.log(response.data.message);
  } catch (error) {
    console.error('Failed to update JSON:', error.response ? error.response.data : error);
  }
}

onMounted(() => {
  fetchJsonList();
  // There is no direct equivalent of `this.$props` in <script setup>, so omit console for props
  // If needed, define props via defineProps.
});
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
</style>