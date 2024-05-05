<template>
  <div class="body">
    <nav class="nav flex">
      <button class="temp-button" @click="updateJSON">Update JSON</button>
      <Dropdown class="" :files="jsonFiles" @selected="handleFileSelection" />
    </nav>
    <section v-if="selectedData">
      <div v-for="item in selectedData" :key="item.id" class="flex-col">
        <FormString :key="prop" :value="item" :property="prop" v-for="prop in editableProperties"
          @update="updateFeature(item.id, $event)" />
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
      jsonRaw: import.meta.env.VITE_TEST_NAME,
      API: import.meta.env.VITE_DATACENTER_API,
      jsonFiles: [],
      selectedData: [],
      editableProperties: ['id', 'title', 'type', 'address', 'latitude', 'longitude', 'auid', 'placeid', 'layout']
    };
  },
  created() {
    this.fetchJsonFiles();
  },
  methods: {
    fetchJsonFiles() {
      axios.get(`${this.API}/json-files`)
        .then(response => {
          this.jsonFiles = response.data.map(file => file.replace(/\.json$/, ''));
        })
        .catch(error => {
          console.error('Error fetching JSON files:', error);
        });
    },
    handleFileSelection(file) {
      axios.get(`${this.API}/json-data/${file}`)
        .then(response => {
          this.selectedData = response.data;
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
    }
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
</style>