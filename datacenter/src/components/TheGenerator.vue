<template>
  <div class="body">
    <button @click="fetchStoresJSON">fetchStoresJSON</button>
    <div class="dashboard-frame">
      <div class="button-set">
        <label for="file-input" class="temp-button">Upload JSON</label>
        <!-- Custom Button -->
        <input type="file" id="file-input" @change="uploadJSON" class="hide" />
        <!-- Actual Input -->
        <button class="temp-button" @click="saveJSON">Save JSON</button>
      </div>
      <h2>Number of Features: {{ jsonData.features.length }}</h2>
      <div class="data-section" v-for="feature in jsonData.features" :key="feature.properties.id">
        <h3>{{ feature.properties.title }}</h3>
        <TheForm :value="feature.properties" property="title" @update="updateFeature(feature.properties.id, $event)" />
        <div class="form-set">
          <TheForm :value="feature.properties" property="type" @update="updateFeature(feature.properties.id, $event)" />
          <TheForm :value="feature.properties" property="layout" @update="updateFeature(feature.properties.id, $event)" />
        </div>

        <TheForm :value="feature.properties" property="description"
          @update="updateFeature(feature.properties.id, $event)" />
        <div class="form-set">
          <TheForm :value="feature.properties" property="address"
            @update="updateFeature(feature.properties.id, $event)" />

          <TheForm :value="feature.geometry.coordinates" property="0"
            @update="updateCoordinates(feature.properties.id, 0, $event)" />

          <TheForm :value="feature.geometry.coordinates" property="1"
            @update="updateCoordinates(feature.properties.id, 1, $event)" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TheForm from "./TheForm.vue";
import * as turf from "@turf/turf";
import axios from 'axios';

export default {
  components: { TheForm },
  data() {
    return {
      jsonData: { features: [] },
      editingFeature: null,
      editingFeatureId: null, // The ID of the feature being edited
      editingProperty: null, // The property of the feature being edited ('title' or 'layout')
    };
  },
  methods: {
    async fetchStoresJSON() {
      const jsonUrl = import.meta.env.VITE_MAP_STORES;
      try {
        const response = await axios.get(jsonUrl);
        this.jsonData = response.data;
        console.log('jsonUrl:', jsonUrl);
      } catch (error) {
        console.error('Failed to fetch stores.json:', error);
      }
    },

    uploadJSON(event) {
      const file = event.target.files[0];
      const reader = new FileReader();

      reader.onload = (e) => {
        this.jsonData = JSON.parse(e.target.result);
      };

      reader.readAsText(file);
    },
    editFeature(id, property) {
      this.editingFeatureId = id;
      this.editingProperty = property;
      this.editingFeature = this.jsonData.features.find(
        (feature) => feature.properties.id === id
      ).properties;
    },
    updateFeature(id, [property, value]) {
      const feature = this.jsonData.features.find(
        (feature) => feature.properties.id === id
      ).properties;
      feature[property] = value;
    },
    updateCoordinates(id, index, value) {
      const feature = this.jsonData.features.find(
        (feature) => feature.properties.id === id
      );
      feature.geometry.coordinates[index] = parseFloat(value);
    },
    saveFeature() {
      this.editingFeature = null;
      this.editingFeatureId = null;
      this.editingProperty = null;
    },

    async saveJSON() {
      try {
        // Use axios to send a POST request to your Flask endpoint
        const response = await axios.post('http://127.0.0.1:5000/save_json', this.jsonData);
        console.log(response.data.message); // Log the success message from Flask
      } catch (error) {
        console.error('Failed to save JSON:', error.response ? error.response.data : error);
      }
    },


    centralizePolygon() {
      // ↓ Calculate the centroid of the polygon using turf
      const center = turf.centroid(feature.geometry);
    },
  },
};
</script>

<style lang="scss" scoped>
.body {
  flex-direction: column;
  align-items: center;
  padding: 80px;
  width: 100vw;
  height: 100%;
  gap: 24px;
}

.dashboard-frame {
  flex-direction: column;
  align-items: flex-start;
  gap: 24px;
}

.data-section {
  flex-direction: column;
  align-items: flex-start;
  gap: 24px;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid var(--token-secondary-text, rgba(255, 255, 255, 0.75));
}

.button-set {
  align-items: flex-start;
  gap: 20px;
}

.form-set {
  align-items: flex-start;
  gap: 24px;
}

// Temp

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

.hide {
  display: none;
}

.text-button {
  cursor: pointer;
  color: var(--2-brand-gray, #808cab);
  background-color: transparent;

  font-family: Be Vietnam Pro;
  font-size: 15px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;
}
</style>