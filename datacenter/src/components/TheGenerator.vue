<template>
  <div class="body">
    <nav class="nav">
      <button class="temp-button" @click="updateJSON">Update JSON</button>
      <button class="temp-button" @click="addNewFeature">Add New Feature</button>
      <Dropdown class="" :files="jsonList" @selected="handleFileSelection" />
    </nav>
    <section v-if="selectedData" class="flex flex-col wrapper">
      <nav class="nav">
        <h2>Number of Features: {{ selectedData.length }}</h2>
        <div class="button-set">
          <LeftArrow @click="prevPage" :disabled="currentPage === 1" />
          <span>{{ currentPage }} / {{ totalPages }}</span>
          <RightArrow @click="nextPage" :disabled="currentPage === totalPages" />
        </div>
      </nav>
      <!-- Extract features in the json -->
      <div class="data-section flex-col" v-for="feature in paginatedFeatures" :key="feature.id">
        <h3>{{ feature.title }}</h3>
        <h4 class="green">Basic</h4>
        <div class="flex-wrap wrapper">
          <FormString :key="prop" :value="feature" :property="prop" v-for="prop in basicProperties"
            @update="updateFeature(feature.id, $event)" />
        </div>
        <div class="splitline" />

        <h4 class="green">Geo</h4>
        <div class="flex-wrap wrapper">
          <FormString :key="prop" :value="feature" :property="prop" v-for="prop in geoProperties"
            @update="updateFeature(feature.id, $event)" />
        </div>
        <div class="splitline" />

        <div v-for="product in products" class="flex-col wrapper">
          <h4 class="green">{{ product }}</h4>

          <div class="flex-wrap wrapper">
            <div v-for="prop in productProperties">
              <FormStringNest :key="prop" :value="feature[product][prop]" :property="prop"
                @update="updateNestedObj(feature.id, product, $event)" />
            </div>
          </div>
        </div>

        <div>
          <h4>Business Hours</h4>
          <div>{{ feature.businesshour }}</div>
        </div>

      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';
// Button
import Dropdown from "./Button/Dropdown.vue";
import RightArrow from "./Button/RightArrow.vue";
import LeftArrow from "./Button/LeftArrow.vue";
// Components
import FormString from "./FormString.vue";
import FormStringNest from "./FormStringNest.vue";
import FormBusinessHour from "./FormBusinessHour.vue";

export default {
  components: { Dropdown, RightArrow, LeftArrow, FormString, FormStringNest, FormBusinessHour },
  data() {
    return {
      API: import.meta.env.VITE_DATACENTER_API,
      jsonList: [],
      selectedData: [],
      currentFile: '',
      basicProperties: ['id', 'title', 'type', 'layout', 'icon', 'description', 'storefront-day', 'storefront-night'],
      geoProperties: ['address', 'latitude', 'longitude', 'auid', 'placeid'],
      timeProperties: [],
      products: ['item1', 'item2', 'item3', 'item4', 'item5'],
      productProperties: ['name', 'description', 'image', 'price'],

      // Page data
      currentPage: 1,
      featuresPerPage: 10,
    };
  },
  created() {
    this.fetchJsonList();
  },
  mounted() {
    console.log('Mounted FormString with props:', this.$props);
  },

  // Pagination
  computed: {
    totalPages() {
      return Math.ceil(this.selectedData.length / this.featuresPerPage);
    },
    paginatedFeatures() {
      let start = (this.currentPage - 1) * this.featuresPerPage;
      let end = start + this.featuresPerPage;
      return this.selectedData.slice(start, end);
    }
  },

  methods: {
    async fetchJsonList() {
      axios.get(`${this.API}/json-files`)
        .then(response => {
          this.jsonList = response.data.map(file => file.replace(/\.json$/, ''));
        })
        .catch(error => {
          console.error('Error fetching JSON files:', file, error);
        });
    },
    handleFileSelection(file) {
      axios.get(`${this.API}/json-data/${file}`)
        .then(response => {
          // 🐞 Debug console
          console.log(this.selectedData);
          this.selectedData = response.data;
          this.currentFile = file;
        })
        .catch(error => {
          console.error('Error fetching JSON data for file:', file, error);
        });
    },

    // Editing data
    updateFeature(featureId, [prop, value]) {
      let feature = this.selectedData.find(f => f.id === featureId);
      if (feature) {
        feature[prop] = value;
      }
    },

    /** 
    *  In Vue, when updating a value inside a nested object, the entire object should be updated
    *  to ensure reactivity. This function updates a specific property within a nested object 
    *  (like 'item1', 'item2', etc.) of a feature in the `selectedData` array. Even though only 
    *  a single property value is being updated, we modify the whole nested object to maintain Vue's reactivity.
    */
    updateNestedObj(featureId, product, [prop, value]) {
      let feature = this.selectedData.find(f => f.id === featureId);
      if (feature && feature[product]) {
        feature[product][prop] = value;
      }
    },

    /** 
    *  wip: edit time
    */
    updateBusinessHour(featureId, [dayIndex, dayKey, value]) {
      let feature = this.selectedData.find(f => f.id === featureId);
      if (feature) {
        feature.businesshour[dayIndex][dayKey] = value;
      }
    },

    updateBusinessHourSlot(featureId, [dayIndex, dayKey, slotIndex, slotKey, value]) {
      let feature = this.selectedData.find(f => f.id === featureId);
      if (feature) {
        feature.businesshour[dayIndex][dayKey][slotIndex][slotKey] = value;
      }
    },

    addBusinessHourSlot(featureId, [dayIndex, dayKey]) {
      let feature = this.selectedData.find(f => f.id === featureId);
      if (feature) {
        feature.businesshour[dayIndex][dayKey].push({ Start: '', Finish: '' });
      }
    },

    removeBusinessHourSlot(featureId, [dayIndex, dayKey, slotIndex]) {
      let feature = this.selectedData.find(f => f.id === featureId);
      if (feature) {
        feature.businesshour[dayIndex][dayKey].splice(slotIndex, 1);
      }
    },


    addNewFeature() {
      if (this.selectedData.length === 0) {
        console.warn('No features available to duplicate.');
        return;
      }

      // Clone the latest feature
      const latestFeature = this.selectedData[this.selectedData.length - 1];
      const newFeature = JSON.parse(JSON.stringify(latestFeature));

      // Generate a new unique ID for the new feature
      newFeature.id = this.selectedData.length + 1;

      // Add the new feature to the selectedData array
      this.selectedData.push(newFeature);
    },

    // Pagination
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },

    async updateJSON() {
      try {
        const filename = this.currentFile;
        const response = await axios.post(`${this.API}/save/${filename}`, this.selectedData);
        // 🐞 Debug console
        // console.log(response.data.message);
      } catch (error) {
        console.error('Failed to update JSON:', error.response ? error.response.data : error);
      }
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
  gap: 24px;
}

.button-set {
  align-items: flex-start;
  gap: 24px;
}
</style>