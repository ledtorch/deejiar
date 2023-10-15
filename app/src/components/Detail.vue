<template>
  <div class="body">
    <!-- Carousel Content -->
    <div v-if="currentPage === 0" class="cover" :style="{ 'backgroundImage': frontStoreImage }">
      <LeftArrow @click="previousPage" class="left-arrow"></LeftArrow>
      <Home @click="toHomePage" class="home-btn"></Home>
      <Share @click="share" class="share-btn"></Share>
      <RightArrow @click="nextPage" class="right-arrow"></RightArrow>
    </div>
    <div v-else class="cover" :style="{ 'backgroundImage': rootUrl(currentItem.image) }">
      <LeftArrow @click="previousPage" class="left-arrow"></LeftArrow>
      <DetailHome @click="toDetailHomePage" class="home-btn"></DetailHome>
      <RightArrow @click="nextPage" class="right-arrow"></RightArrow>
    </div>

    <!-- Cover Page -->
    <div v-if="currentPage === 0" class="content">
      <div class=" items-frame">
        <div class="leftImage" :style="{ 'backgroundImage': item1 }"></div>
        <div class="rightImage" :style="{ 'backgroundImage': item2 }"></div>
      </div>
      <div class="content-frame">
        <div class="title-block">
          <h2 class="stretch">{{ storeTitle }}</h2>
          <TagShopType :store="data" />
        </div>
        <p class="state">{{ description }}</p>
      </div>
      <Businesshour :bizTime="data.businesshour" viewMode="overview" />
      <div class="splitline"></div>
      <div class="content-frame">
        <Businesshour :bizTime="data.businesshour" viewMode="detail" />
      </div>
      <div class="content-frame">
        <Address :address="data.address" />
      </div>
      <div class="splitline"></div>
    </div>

    <!-- Product Page -->
    <div v-else class="content">
      <div class="title-block">
        <h2 class="stretch">{{ currentItem.name }}</h2>
        <h2>{{ currentItem.price }}</h2>
      </div>
      <p class="state">{{ currentItem.description }}</p>
    </div>

  </div>
</template>
  
<script>
// Components
import Home from "./Button/Icon/Home.vue";
import DetailHome from "./Button/Icon/DetailHome.vue";
import Share from "./Button/Icon/Share.vue";
import LeftArrow from "./Button/Icon/LeftArrow.vue";
import RightArrow from "./Button/Icon/RightArrow.vue";
import TagShopType from "./Button/TagShopType.vue";
import Review from "./Sheet/Review.vue";
import Businesshour from "./Sheet/Businesshour.vue";
import Address from "./Sheet/Address.vue";
// 🏗️ TODO: Share Feature
// Vue Utilities and Plugins
import { useMeta } from 'vue-meta';
import { useRouter } from "vue-router";
import { ref, computed, watchEffect } from 'vue';

export default {
  components: { Home, DetailHome, Share, LeftArrow, RightArrow, TagShopType, Review, Businesshour, Address },
  data() {
    return {
      storeTitle: '',
      description: '',
      storeType: '',
      data: null,
      currentPage: 0,
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

    this.data = storeData.properties;
    this.storeTitle = this.data.title;
    this.description = this.data.description;
    this.storeType = this.data.type;
  },
  computed: {
    storeLayout() {
      // // 🐞 Debug console
      // console.log("Compute storeLayout: " + this.store?.layout);
      return this.data?.layout;
    },
    frontStoreImage() {
      return this.rootUrl(this.data?.storefront.day);
    },
    item1() {
      return this.rootUrl(this.data?.item1.image);
    },
    item2() {
      return this.rootUrl(this.data?.item2.image);
    },
    item3() {
      return this.rootUrl(this.data?.item3.image);
    },
    item4() {
      return this.rootUrl(this.data?.item4.image);
    },
    item5() {
      return this.rootUrl(this.data?.item5.image);
    },
    currentItem() {
      return this.data[`item${this.currentPage}`];
    },

    totalPages() {
      let count = 1;  // Start with 1 for the DetailHomePage
      for (let i = 1; i <= 5; i++) {
        if (this.data[`item${i}`]?.name) {
          count++;
        }
      }
      return count;
    },
    // Define the pages
    currentItem() {
      // 🏗️ TODO: Make a debug console to print totalPages

      // If currentPage is 0 or the item doesn't exist, return an empty object
      if (this.currentPage === 0 || !this.data[`item${this.currentPage}`]) {
        return {};
      }
      return this.data[`item${this.currentPage}`];
    },
  },
  methods: {
    rootUrl(imagePath) {
      const baseUrl = `${window.location.protocol}//${window.location.host}`;
      return `url('${baseUrl}/${imagePath}')`;
    },
    nextPage() {
      this.currentPage = (this.currentPage + 1) % this.totalPages;
    },
    previousPage() {
      this.currentPage = (this.currentPage + this.totalPages - 1) % this.totalPages;
    },
    toHomePage() {
      this.$router.push('/');
    },
    toDetailHomePage() {
      this.currentPage = 0;
    },
    share() {
      const text = encodeURIComponent('I check ' + this.storeTitle + ' with Deejia!');
      const url = encodeURIComponent('\n' + window.location.href);
      const twitterUrl = `https://twitter.com/intent/tweet?text=${text}&url=${url}`;
      window.open(twitterUrl, '_blank');
    },
  },
};
</script>

<style lang="scss" scoped>
// Frame
.body {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  overflow-y: auto;

  /* Media query for screen widths 430px and below */
  @media (max-width: 430px) {
    padding-bottom: 99px;
  }
}

.content {
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
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
  position: relative;
  width: 100%;

  // Maintains 1:1 aspect ratio
  padding-top: 100%;

  // Image setting
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.leftImage {
  align-items: center;
  // width: 100px;
  width: 66%;
  height: 100px;
  border-radius: 12px;

  // Image setting
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.rightImage {
  align-items: center;
  // width: 100px;
  width: 34%;
  height: 100px;
  border-radius: 12px;

  // Image setting
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

.items-frame {
  align-items: flex-start;
  width: 100%;
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

// Button
.left-arrow,
.right-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.left-arrow {
  left: 12px;
}

.right-arrow {
  right: 12px;
}

.home-btn {
  position: absolute;
  left: 12px;
  top: 12px;
}

.share-btn {
  position: absolute;
  right: 12px;
  top: 12px;
}
</style>
  