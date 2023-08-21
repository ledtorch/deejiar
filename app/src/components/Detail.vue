<template>
  <div>
    <div class="cover" :style="cover"></div>
    <div class="title-block">
      <h2 class="stretch">{{ store ? store.title : "" }}</h2>
      <TagShopType :store="store" />
    </div>
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
  </div>
</template>
  
<script>
import { useRoute } from "vue-router";
export default {
  props: ["title"],
  data() {
    return {
      description: null,
    };
  },

  computed: {
    cover() {
      const type = this.store?.storefront; // Set Taco as default png to prevent the undefined msg
      const path = `/Icon/category/${type}.png`;
      console.log("🆗 Component -> TagShopType, Icon Path: " + path);
      return `background: url('${path}') center/cover no-repeat; width: 24px; height: 24px;`;
    },
  },

  async mounted() {
    // Decode the title from the URL
    const route = useRoute();
    const title = route.params.title;
    const decodedTitle = decodeURIComponent(title);

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
  
<style lang="scss" scoped>
.cover {
  align-items: center;
  width: 100%;
  height: 100%;
}
</style>
  