<!-- Store.vue -->
<template>
  <div>
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
  </div>
</template>
  
  <script>
export default {
  props: ["title"],
  data() {
    return {
      description: null,
    };
  },
  async mounted() {
    // Decode the title from the URL
    const decodedTitle = decodeURIComponent(this.title);

    // Fetch store details based on the decoded title
    const response = await fetch(`/stores.json`);
    const stores = await response.json();
    const store = stores.features.find(
      (store) => store.properties.title === decodedTitle
    );
    if (store) {
      this.description = store.properties.description;
    }
  },
};
</script>
  
  <style>
/* Add your styles here */
</style>
  