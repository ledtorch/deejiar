<template>
  <div class="body">
    <div class="dashboard-frame">

      <div class="button-set">
        <button @click="editJSON">Edit JSON from Server</button>
        <button class="temp-button" @click="updateJSON">Update JSON</button>
      </div>

      <h2>Number of Features: {{ jsonData.features.length }}</h2>

      <div class="data-section" v-for="feature in jsonData.features" :key="feature.properties.id">
        <h3>{{ feature.properties.title }}</h3>
        <TheForm :value="feature.properties" property="title" @update="updateFeature(feature.properties.id, $event)" />
        <TheForm :value="feature.properties" property="auid" @update="updateFeature(feature.properties.id, $event)" />

        <div class="form-set">
          <!-- Editing icons -->
          <div>
            <input type="text" v-model="iconBase" placeholder="Enter icon base e.g., FormosanNoodles"
              @change="updateIcons(feature.properties.id)" />
          </div>
          <TheForm :value="feature.properties" property="type" @update="updateFeature(feature.properties.id, $event)" />
          <TheForm :value="feature.properties" property="layout" @update="updateFeature(feature.properties.id, $event)" />
        </div>
        <!-- Storefront -->
        <div class="form-set">
          <TheForm :value="feature.properties.storefront" property="day"
            @update="updateStorefront(feature.properties.id, 'day', $event)" />
          <TheForm :value="feature.properties.storefront" property="night"
            @update="updateStorefront(feature.properties.id, 'night', $event)" />

        </div>
        <TheForm :value="feature.properties" property="description"
          @update="updateFeature(feature.properties.id, $event)" />

        <!-- Items -->
        <div v-for="itemIndex in 5" :key="`item${itemIndex}`">
          <TheForm :value="feature.properties" :property="`item${itemIndex}`"
            @update="updateFeatureItem(feature.properties.id, `item${itemIndex}`, $event)" />
        </div>

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
import axios from 'axios';

export default {
  components: { TheForm },
  data() {
    return {
      jsonUrl: import.meta.env.VITE_MAP_STORES,
      // Initialize jsonData for GeoJSON FeatureCollection format with an empty features array
      jsonData: { features: [] },
      editingFeature: null,
      editingFeatureId: null, // The ID of the feature being edited
      editingProperty: null // The property of the feature being edited ('title' or 'layout')
    };
  },
  methods: {
    async editJSON() {
      try {
        const response = await axios.get(this.jsonUrl);
        this.jsonData = response.data;
        // 🐞 Debug console
        console.log('Fetched URL:', this.jsonUrl);
        console.log('Fetched data:', response.data);
        console.log('jsonData:', this.jsonData);
      } catch (error) {
        console.error('Failed to fetch stores.json:', error);
      }
    },
    async updateJSON() {
      try {
        const response = await axios.post(this.jsonUrl, this.jsonData);
        // 🐞 Debug console, the confirm message from 'Flask'
        console.log(response.data.message);
      } catch (error) {
        console.error('Failed to update stores.json:', error.response ? error.response.data : error);
      }
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
    }
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
