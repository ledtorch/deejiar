<template>
  <div class="body">
    <div class="cover" :style="{ 'backgroundImage': mainColumnImage }"></div>
    <div class="content">
      <div class=" content-frame">
        <div class="title-block">
          <h2 class="stretch">{{ storeTitle }}</h2>
          <TagShopType :store="data" />
        </div>
        <p class="state">{{ description }}</p>
        <Businesshour :bizTime="data.businesshour" viewMode="overview" />
      </div>
      <div class="splitline"></div>
      <div class="content-frame">
        <Businesshour :bizTime="data.businesshour" viewMode="detail" />
      </div>
      <div class="content-frame">
        <Address :address="data.address" />
      </div>
      <div class="splitline"></div>
    </div>
  </div>
</template>
  
<script>
import IconButtonClose from "./Button/IconButtonClose.vue";
import TagShopType from "./Button/TagShopType.vue";
import Review from "./Sheet/Review.vue";
import Businesshour from "./Sheet/Businesshour.vue";
import Address from "./Sheet/Address.vue";

export default {
  components: { IconButtonClose, TagShopType, Review, Businesshour, Address },
  data() {
    return {
      storeTitle: '',
      description: '',
      storeType: '',
      data: null, // Initialize this as null
    }
  },
  async created() {
    // Fetch url title and decode it
    const urlTitle = decodeURIComponent(this.$route.params.title);

    // Define root: https://root.com
    const rootURL = `${window.location.protocol}//${window.location.host}`;

    const response = await fetch(`${rootURL}/stores.json`);
    const stores = await response.json();
    console.log("Fetched JSON data: ", stores);

    // Find the store matching the title from the URL
    const storeData = stores.features.find(store => store.properties.title === urlTitle);
    console.log("The storeData: ", storeData);

    // If a matching store is found, update the component's data
    if (storeData) {
      console.log('storeData: ' + storeData)
      this.data = storeData.properties;
      this.storeTitle = storeData.properties.title;
      this.description = storeData.properties.description;
      this.storeType = storeData.properties.type;
    }
  },
  methods: {
    backgroundImageUrl(imagePath) {
      const baseUrl = `${window.location.protocol}//${window.location.host}`;
      return `url('${baseUrl}/${imagePath}')`;
    }
  },
  computed: {

    storeLayout() {
      // // 🐞 Debug console
      // console.log("Compute storeLayout: " + this.store?.layout);
      return this.data?.layout;
    },

    mainColumnImage() {
      return this.backgroundImageUrl(this.data.storefront);
    },
    item1() {
      return this.backgroundImageUrl(this.data?.item1.image);
    },
    item2() {
      return this.backgroundImageUrl(this.data?.item2.image);
    },
    item3() {
      return this.backgroundImageUrl(this.data?.item3.image);
    },
    item4() {
      return this.backgroundImageUrl(this.data?.item4.image);
    },
    item5() {
      return this.backgroundImageUrl(this.data?.item5.image);
    }
  },
};
</script>

<style lang="scss" scoped>
.body {
  position: relative;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  margin-bottom: 133px;
}

.content {
  overflow-y: auto;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  height: 100%;
  padding: 20px;
  gap: 24px;
}

.title-block {
  align-items: flex-start;
  justify-content: flex-start;
  align-content: flex-start;
  align-self: stretch;
  flex-wrap: wrap;
  flex: 1 0 0;
  gap: 12px;
}

.cover {
  align-items: center;
  width: 100%;
  height: 100%;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}


.stretch {
  flex: 1 0 0;
}

.content-frame {
  flex-direction: column;
  gap: 12px;
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
  