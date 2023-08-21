<template>
  <div>
    <input type="file" @change="uploadJSON" />
    <table>
      <tr v-for="feature in jsonData.features" :key="feature.properties.id">
        <td>{{ feature.properties.title }}</td>
        <td>
          <button @click="editFeature(feature.properties.id)">Edit</button>
        </td>
      </tr>
    </table>
    <div v-if="editingFeature">
      <input v-model="editingFeature.title" />
      <button @click="saveFeature">Save</button>
    </div>
    <button @click="downloadJSON">Download JSON</button>
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

<style lang="sass" scoped>
</style>
