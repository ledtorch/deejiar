<template>
  <div class="body flex-col">
    <!-- Carousel Content -->
    <div v-if="currentPage === 0" class="cover" :style="{ 'backgroundImage': storeFrontImage }">
      <LeftArrow @click="previousPage" class="left-arrow" />
      <Home @click="toHomePage" class="home-btn" />
      <Share @click="share" class="share-btn" />
      <RightArrow @click="nextPage" class="right-arrow" />
    </div>
    <div v-else class="cover" :style="{ 'backgroundImage': rootUrl(currentItem.image) }">
      <LeftArrow @click="previousPage" class="left-arrow" />
      <HomeToDetail @click="toDetailHomePage" class="home-btn" />
      <RightArrow @click="nextPage" class="right-arrow" />
    </div>

    <!-- Cover Page -->
    <div v-if="currentPage === 0" class="content flex-col">
      <div class="items-frame">
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
      <GetDirection variant="apple" :appleAUID="appleAUID"></GetDirection>
      <GetDirection variant="google" :storeTitle="storeTitle"></GetDirection>
      <!-- // 🏗️ TODO -->
      <!-- <GetDirection variant="google" :googlePlaceid="googlePlaceid"></GetDirection> -->
    </div>

    <!-- Product Page -->
    <div v-else class="content flex-col">
      <div class="title-block">
        <h2 class="stretch">{{ currentItem.name }}</h2>
        <h2>{{ currentItem.price }}</h2>
      </div>
      <!-- Use v-html to render <br> -->
      <p class="state" v-html="currentItem.description"></p>
      <GetDirection variant="apple" :appleAUID="appleAUID"></GetDirection>
      <GetDirection variant="google" :storeTitle="storeTitle"></GetDirection>
      <!-- // 🏗️ TODO -->
      <!-- <GetDirection variant="google" :googlePlaceid="googlePlaceid", ></GetDirection> -->
    </div>

  </div>
</template>

<script>
// Components
import TagShopType from "./Button/TagShopType.vue";
import Review from "./Sheet/Review.vue";
import Businesshour from "./Sheet/Businesshour.vue";
import Address from "./Sheet/Address.vue";
// Buttons
import Home from "./Button/Icon/Home.vue";
import HomeToDetail from "./Button/Icon/HomeToDetail.vue";
import Share from "./Button/Icon/Share.vue";
import LeftArrow from "./Button/Icon/LeftArrow.vue";
import RightArrow from "./Button/Icon/RightArrow.vue";
import GetDirection from "./Button/CTA/GetDirection.vue";

export default {
  components: { Home, HomeToDetail, Share, LeftArrow, RightArrow, TagShopType, Review, Businesshour, Address, GetDirection },
  data() {
    return {
      storeTitle: '',
      description: '',
      storeType: '',
      // The data from the JSON file
      data: '',
      appleAUID: '',
      googlePlaceid: '',
      geoData: '',
      currentPage: 0,

      // Lazy loading
      lazyloadingImage: '/images/loading-placeholder.webp'
    }
  },

  async created() {
    // Fetch url title and decode it
    const urlTitle = decodeURIComponent(this.$route.params.title);

    // Define root: https://root.com
    const rootURL = `${window.location.protocol}//${window.location.host}`;

    // const response = await fetch(`${rootURL}/stores.json`);
    const response = await fetch(`${rootURL}/stores.json?v=${new Date().getTime()}`);
    const stores = await response.json();
    console.log("Fetched JSON data: ", stores);

    // Find the store matching the title from the URL
    const storeData = stores.features.find(store => store.properties.title === urlTitle);
    console.log("The storeData: ", storeData);

    // Testing
    const geoData = storeData.geometry.coordinates;
    const formattedCoordinates = `${geoData[1]}%2C${geoData[0]}`;
    console.log('formattedCoordinates', formattedCoordinates);
    // Testing

    this.data = storeData.properties;
    this.appleAUID = storeData.properties.auid;
    this.googlePlaceid = storeData.properties.placeid;
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
    storeFrontImage() {
      // Defaults to an empty string before the app renders without data 
      const storeFrontDayData = this.data?.storefront?.day || '';
      return this.rootUrl(storeFrontDayData);
      // return this.rootUrl(this.data?.storefront.day);
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
      // Start with 1 for the DetailHomePage
      let count = 1;
      for (let i = 1; i <= 5; i++) {
        if (this.data[`item${i}`]?.name) {
          count++;
        }
      }
      return count;
    },
    // Define the pages
    currentItem() {
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
      const text = encodeURIComponent('I check ' + this.storeTitle + ' with Deejiar!');
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
  width: 100vw;
  height: 100vh;
  overflow-y: auto;

  /* Media query for screen widths 430px and below */
  @media (max-width: 430px) {
    padding-bottom: 99px;
  }
}

.content {
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
