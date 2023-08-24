<template>
  <div class="body">
    <div class="button-set">
      <label for="file-input" class="temp-button">Upload JSON</label>
      <!-- Custom Button -->
      <input type="file" id="file-input" @change="uploadJSON" class="hide" />
      <!-- Actual Input -->
      <button class="temp-button" @click="downloadJSON">Download JSON</button>
    </div>

    <table class="table">
      <p>Number of Features: {{ numberOfFeatures }}</p>
      <tr v-for="feature in jsonData.features" :key="feature.properties.id">
        <td>{{ feature.properties.title }}</td>
        <td>
          <button
            class="text-button"
            @click="editFeature(feature.properties.id)"
          >
            Edit
          </button>
        </td>
        <td>{{ feature.properties.layout }}</td>
        <td>
          <button
            class="text-button"
            @click="editFeature(feature.properties.id)"
          >
            Edit
          </button>
        </td>
      </tr>
    </table>
    <div class="form" v-if="editingFeature">
      <input v-model="editingFeature.title" />
      <button class="text-button" @click="saveFeature">Save</button>
      <input v-model="editingFeature.layout" />
      <button class="text-button" @click="saveFeature">Save</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      jsonData: { features: [] }, // Define jsonData with a default structure
      editingFeature: null, // Define editingFeature with a default value
    };
  },
  computed: {
    numberOfFeatures() {
      return this.jsonData.features.length;
    },
  },
  methods: {
    uploadJSON(event) {
      const file = event.target.files[0];
      const reader = new FileReader();

      reader.onload = (e) => {
        this.jsonData = JSON.parse(e.target.result);
      };

      reader.readAsText(file);
    },
    editFeature(id) {
      this.editingFeature = this.jsonData.features.find(
        (feature) => feature.properties.id === id
      ).properties;
    },
    saveFeature() {
      // Save logic here
      this.editingFeature = null;
    },
    downloadJSON() {
      const dataStr =
        "data:text/json;charset=utf-8," +
        encodeURIComponent(JSON.stringify(this.jsonData));
      const downloadAnchorNode = document.createElement("a");

      downloadAnchorNode.setAttribute("href", dataStr);
      downloadAnchorNode.setAttribute("download", "data.json");
      document.body.appendChild(downloadAnchorNode);
      downloadAnchorNode.click();
      downloadAnchorNode.remove();
    },
  },
};
</script>

<style lang="scss" scoped>
.body {
  flex-direction: column;
  align-items: center;
  width: 100vw;
  height: 100%;
  padding: 100px 100px;
  gap: 100px;
}

.table {
  gap: 120px;
}

.form {
  justify-content: space-between;
  align-items: center;
  width: auto;
  padding: 12px;
  border-radius: var(--border-content, 6px);
  background: var(--4-base-dark-base, rgba(255, 255, 255, 0.07));
}

.button-set {
  align-items: flex-start;
  gap: 20px;
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
