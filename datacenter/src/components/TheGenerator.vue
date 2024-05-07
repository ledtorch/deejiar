<template>
  <div class="body">
    <nav class="nav">
      <button class="temp-button" @click="updateJSON">Update JSON</button>
      <Dropdown class="" :files="jsonFiles" @selected="handleFileSelection" />
    </nav>
    <section v-if="selectedData">
      <h2>Number of Features: {{ selectedData.length }}</h2>
      <div class="data-section flex-col" v-for="item in selectedData" :key="item.id">
        <div class="form-set flex-wrap">
          <FormString :key="prop" :value="item" :property="prop" v-for="prop in basicProperties"
            @update="updateFeature(item.id, $event)" />
          <FormString :key="prop" :value="item" :property="prop" v-for="prop in geoProperties"
            @update="updateFeature(item.id, $event)" />
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import Dropdown from "./Button/Dropdown.vue";
import FormString from "./FormString.vue";
import axios from 'axios';

export default {
  components: { Dropdown, FormString },
  data() {
    return {
      API: import.meta.env.VITE_DATACENTER_API,
      jsonFiles: [],
      selectedData: [],
      currentFile: '',
      basicProperties: ['id', 'title', 'type', 'layout'],
      geoProperties: ['address', 'latitude', 'longitude', 'auid', 'placeid']
    };
  },
  created() {
    this.fetchJsonFiles();
  },
  methods: {
    async fetchJsonFiles() {
      axios.get(`${this.API}/json-files`)
        .then(response => {
          this.jsonFiles = response.data.map(file => file.replace(/\.json$/, ''));
        })
        .catch(error => {
          console.error('Error fetching JSON files:', file, error);
        });
    },
    handleFileSelection(file) {
      axios.get(`${this.API}/json-data/${file}`)
        .then(response => {
          this.selectedData = response.data;
          this.currentFile = file;
        })
        .catch(error => {
          console.error('Error fetching JSON data for file:', file, error);
        });
    },



    updateFeature(featureId, [prop, value]) {
      let feature = this.selectedData.find(f => f.id === featureId);
      if (feature) {
        feature[prop] = value;
      }
    },
    async updateJSON() {
      try {
        const filename = this.currentFile; // Ensure this is the correct filename
        const response = await axios.post(`${this.API}/save/${filename}`, this.selectedData);
        console.log("Current file to be updated:", this.currentFile);

        console.log(response.data.message);
      } catch (error) {
        console.error('Failed to update JSON:', error.response ? error.response.data : error);
      }
    },

  },
};
// 🐞 Debug console
// console.log('Selected file:', file);
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
  border: 1px solid var(--token-secondary-text, rgba(255, 255, 255, 0.75));
}

.form-set {
  align-self: stretch;
  align-items: flex-start;
  gap: 24px;
}
</style>