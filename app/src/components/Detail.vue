<template>
  <div class="body">
    <div class="cover" :style="cover"></div>
    <TagShopType :store="store" />
    <div class="title-block">
      <h2 class="stretch">{{ title }}</h2>
      <TagShopType :store="store" />
    </div>
    <p class="state">{{ description }}</p>
  </div>
</template>
  
<script>
import { useRoute } from "vue-router";
import IconButtonClose from "./Button/IconButtonClose.vue";
import TagShopType from "./Button/TagShopType.vue";
import Avatar from "./Sheet/Avatar.vue";
import Review from "./Sheet/Review.vue";
import Businesshour from "./Sheet/Businesshour.vue";
export default {
  props: ["store", "title"],
  data() {
    return {
      description: null
    };
  },

  computed: {
    cover() {
      const type = this.store?.storefront;

      const path = `/Icon/category/${type}.png`;
      console.log("🆗 Component -> TagShopType, Icon Path: " + path);
      return `background: url('${path}') center/cover no-repeat; width: 24px; height: 24px;`;
    }
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
      store => store.properties.title === decodedTitle
    );
    if (store) {
      this.description = store.properties.description;
    }
  }
};
</script>
  
<style lang="scss" scoped>
.body {
  flex-direction: column;
  align-items: flex-start;
  padding: 0px 20px 20px 20px;
}
.cover {
  align-items: center;
  width: 100%;
  height: 100%;
}

.state {
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  padding: 12px;
  border-radius: var(--border-button-round, 8px);
  background: var(--4-base-dark-base, rgba(255, 255, 255, 0.07));
}
</style>
  