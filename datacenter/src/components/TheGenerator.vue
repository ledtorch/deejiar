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
        <!-- Title, type and layout -->
        <div class="form-set">
          <FormString v-for="prop in ['id', 'title', 'type', 'layout']" :key="prop" :value="feature.properties"
            :property="prop" @update="updateFeature(feature.properties.id, $event)" />
        </div>

        <!-- Storefront and overview-->
        <div class="form-set">
          <FormString :value="feature.properties.storefront" property="day"
            @update="updateStorefront(feature.properties.id, 'day', $event)" />
          <FormString :value="feature.properties.storefront" property="night"
            @update="updateStorefront(feature.properties.id, 'night', $event)" />
        </div>
        <FormString :value="feature.properties" property="description"
          @update="updateFeature(feature.properties.id, $event)" />

        <!-- Items -->
        <!-- <div v-for="itemIndex in 5" :key="`item${itemIndex}`" class="form-wrap">
          <h3>Item {{ itemIndex }}</h3>
          <FormString v-for="prop in ['name', 'image', 'price', 'description']" :key="`item${itemIndex}-${prop}`"
            :value="feature.properties[`item${itemIndex}`][prop]" :property="`item${itemIndex}.${prop}`"
            @update="newValue => updateFeatureItem(feature.properties.id, `item${itemIndex}.${prop}`, newValue)" />

        </div> -->
        <!-- Simplified Items Display -->
        <div v-for="itemIndex in 5" :key="`item${itemIndex}`" class="form-wrap">
          <h3>Item {{ itemIndex }}</h3>
          <button @click="logItemProperties(feature.properties.id, itemIndex)">Log Item {{ itemIndex }}
            Properties</button>

          <!-- <FormString :value="feature.properties[`item${itemIndex}`]" property="`item${itemIndex}.name`"
            @update="updateFeature(feature.properties.id, $event)" /> -->

          <FormString v-for="prop in ['name', 'price', 'image', 'description']" :key="prop"
            :value="feature.properties[`item${itemIndex}`].prop" :property="prop"
            @update="handlePropertyUpdate(feature.properties.id, $event)" />

        </div>


        <!-- Geo data -->
        <h3>Geo data</h3>
        <div class="form-set">
          <FormString :value="feature.properties" property="auid"
            @update="updateFeature(feature.properties.id, $event)" />
          <FormString :value="feature.properties" property="address"
            @update="updateFeature(feature.properties.id, $event)" />
          <FormArray :value="feature.geometry.coordinates" property="coordinates"
            @update="newValue => updateCoordinates(feature.properties.id, newValue)" />
        </div>
        <h3>Business hour</h3>
      </div>

    </div>
  </div>
</template>

<script>
import FormString from "./FormString.vue";
import FormArray from "./FormArray.vue";
import axios from 'axios';

export default {
  components: { FormString, FormArray },
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
    updateStorefront(id, key, [property, value]) {
      const feature = this.jsonData.features.find(feature => feature.properties.id === id);
      if (feature && feature.properties.storefront) {
        feature.properties.storefront[key] = value;
      } else {
        console.error('Feature or storefront not found');
      }
    },
    updateFeature(id, [property, value]) {
      console.log('Hi!');
      console.log('property: ' + property);
      console.log('value: ' + value);
      const feature = this.jsonData.features.find(
        (feature) => feature.properties.id === id
      ).properties;
      feature[property] = value;
    },
    logItemProperties(id, itemIndex) {
      console.log('Hi!');
      console.log(`LogItemProperties called with id: ${id}, itemIndex: ${itemIndex}`);

      // Find the feature with the given id
      const feature = this.jsonData.features.find(f => f.properties.id === id);
      console.log('Feature: ' + feature.properties.id)
      if (feature) {
        const item = feature.properties[`item${itemIndex}`];
        console.log(`Item ${itemIndex} properties:`, item);

        // If you need to log each property individually:
        ['name', 'image', 'price', 'description'].forEach(prop => {
          console.log(`Item ${itemIndex} ${prop}:`, item[prop]);
        });
      } else {
        console.error(`Feature with id ${id} not found`);
      }
    },


    handlePropertyUpdate(id, [property, value]) {
      console.log('Oh ya!');
      console.log('property: ' + property);
      console.log('value: ' + value);
      const feature = this.jsonData.features.find(
        (feature) => feature.properties.id === id
      ).properties;
      feature[property] = value;
      // const feature = this.jsonData.features.find(f => f.properties.id === id);
      // console.log('Feature: ' + feature.properties.id.name)
      // if (feature) {
      //   const item = feature.properties[`item${itemIndex}`];
      //   console.log(`Item ${itemIndex} properties:`, item);
      // } else {
      //   console.log('failed');
      // }
    },



    updateCoordinates(id, newValue) {
      const feature = this.jsonData.features.find(feature => feature.properties.id === id);
      if (feature) {
        // Directly set the coordinates to the new values assuming newValue is already an array of numbers
        feature.geometry.coordinates = Array.isArray(newValue[1]) ? newValue[1] : newValue;
      }
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
  max-width: 996px;
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
  display: flex;
  align-self: stretch;
  align-items: flex-start;
  gap: 24px;
}

.form-wrap {
  display: flex;
  align-items: flex-start;
  flex-wrap: wrap;
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
