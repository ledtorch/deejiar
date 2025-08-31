<template>
  <main class="body flex-col">
    <!-- Loading Ani -->
    <div v-if="isLoading" class="image-loading-overlay">
      <LoadingAni />
    </div>

    <!-- Carousel Content -->
    <div v-if="currentPage === 0" class="hero-container" :style="{ 'backgroundImage': storeFrontImage }">
      <LeftArrowRound @click="previousPage" class="left-arrow" />
      <Home @click="toHomePage" class="home-btn" />
      <Share @click="share" class="share-btn" />
      <RightArrowRound @click="nextPage" class="right-arrow" />
    </div>
    <div v-else class="hero-container" :style="{ 'backgroundImage': currentItem }">
      <LeftArrowRound @click="previousPage" class="left-arrow" />
      <HomeToDetail @click="toDetailHomePage" class="home-btn" />
      <RightArrowRound @click="nextPage" class="right-arrow" />
    </div>

    <!-- Cover Page -->
    <section v-if="currentPage === 0 && storeProperties" class="content-section">
      <!-- Store data loaded -->
      <div class="products-shortcut">
        <div class="leftImage" :style="{ 'backgroundImage': storeImages.product1 }"></div>
        <div class="rightImage" :style="{ 'backgroundImage': storeImages.product2 }"></div>
      </div>
      <div class="key-info-container">
        <HeaderStore :store="storeProperties" />
        <p class="store-description">{{ detailsJSON.description }}</p>
      </div>
      <Businesshour :bizTime="detailsJSON.businesshour" viewMode="overview" />
      <div class="splitline"></div>
      <!-- <Businesshour :bizTime="detailsJSON.businesshour" viewMode="detail" /> -->
      <Address :address="detailsJSON.address" />
      <div class="splitline"></div>
      <GetDirection variant="apple" :appleAUID="storeProperties.auid"></GetDirection>
      <GetDirection variant="google" :storeTitle="storeProperties.title"></GetDirection>
    </section>

    <!-- Product Page -->
    <section v-else class="content-section">
      <div v-if="currentProduct" class="title-block">
        <h4 class="_stretch">{{ currentProduct.name }}</h4>
        <h4>{{ currentProduct.price }}</h4>
      </div>
      <!-- Use v-html to render <br> -->
      <p v-if="currentProduct" class="store-description" v-html="currentProduct.description"></p>
    </section>

  </main>
</template>

<script setup>
// Components
import Businesshour from "./sheet/Businesshour.vue";
import Address from "./sheet/Address.vue";
import LoadingAni from "./common/LoadingAni.vue";
import HeaderStore from "./nav/HeaderStore.vue";
// Buttons
import Home from "./button/Icon/Home.vue";
import HomeToDetail from "./button/Icon/HomeToDetail.vue";
import Share from "./button/Icon/Share.vue";
import LeftArrowRound from "./button/Icon/LeftArrowRound.vue";
import RightArrowRound from "./button/Icon/RightArrowRound.vue";
import GetDirection from "./button/CTA/GetDirection.vue";

import { ref, watch, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

// Router setup
const route = useRoute();
const router = useRouter();

// Reactive data
const storeTitle = ref('');
const description = ref('');
const storeType = ref('');
// The data from the JSON file
const data = ref('');
const appleAUID = ref('');
const googlePlaceid = ref('');
const geoData = ref('');
const currentPage = ref(0);




// Updated computed properties for new data structure
const storeFrontImage = computed(() => {
  return storeImages.value?.storefront || '';
});

const totalPages = computed(() => {
  // Start with 1 for the DetailHomePage
  let count = 1;
  // Count how many products exist in detailsJSON
  if (detailsJSON.value?.product1?.name) count++;
  if (detailsJSON.value?.product2?.name) count++;
  if (detailsJSON.value?.product3?.name) count++;
  if (detailsJSON.value?.product4?.name) count++;
  if (detailsJSON.value?.product5?.name) count++;
  return count;
});

// Define the current item based on page
const currentItem = computed(() => {
  // If currentPage is 0, return storefront image
  if (currentPage.value === 0) {
    return storeImages.value?.storefront || '';
  }

  // Get the product for current page
  const product = detailsJSON.value?.[`product${currentPage.value}`];
  if (!product?.name) return '';

  // Return the image URL for this product
  const base = storeDetailsEndpoint();
  const safeName = product.name
    .replace(/&/g, 'and')
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-');

  return `url("${base}/${safeName}.jpg")`;
});

// Get current product data for display
const currentProduct = computed(() => {
  if (currentPage.value === 0) return null;
  return detailsJSON.value?.[`product${currentPage.value}`] || null;
});

// Methods
const rootUrl = (imagePath) => {
  const baseUrl = `${window.location.protocol}//${window.location.host}`;
  return `url('${baseUrl}/${imagePath}')`;
};

const nextPage = () => {
  currentPage.value = (currentPage.value + 1) % totalPages.value;
};

const previousPage = () => {
  currentPage.value = (currentPage.value + totalPages.value - 1) % totalPages.value;
};

const toHomePage = () => {
  router.push('/map');
};

const toDetailHomePage = () => {
  currentPage.value = 0;
};

const share = () => {
  const text = encodeURIComponent('I check ' + storeTitle.value + ' with Deejiar!');
  const url = encodeURIComponent('\n' + window.location.href);
  const twitterUrl = `https://twitter.com/intent/tweet?text=${text}&url=${url}`;
  window.open(twitterUrl, '_blank');
};

// JSON Endpoints
const mapEndpoint = (path) => {
  return `${import.meta.env.VITE_API_URL}/map/${path}`;
};

const storeProperties = ref(null);
const detailsJSON = ref(null);
const isLoading = ref(true);
const error = ref(null);

// Store Details Endpoint function
const storeDetailsEndpoint = () => {
  if (!storeProperties.value) return '';
  const { id, type, title } = storeProperties.value;
  const country = id.split('_')[0];
  const safeTitle = title
    .replace(/&/g, 'and')
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-');
  return `${import.meta.env.VITE_CDN_URL}/stores/${country}/${type}/${safeTitle}`;
};

// Computed property for store images
const storeImages = computed(() => {
  if (!detailsJSON.value || !storeProperties.value) return null;

  const base = storeDetailsEndpoint();
  const safe = (product) => {
    const name = product?.name;
    return name
      ? name
        .replace(/&/g, 'and')               // Convert & to "and"
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, '')    // Remove diacritics
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')           // Remove punctuation
        .replace(/\s+/g, '-')               // Replace spaces with hyphens
      : null;
  };

  const safeName1 = safe(detailsJSON.value?.product1);
  const safeName2 = safe(detailsJSON.value?.product2);

  return {
    storefront: `url("${base}/storefront-day.jpg")`,
    product1: safeName1 ? `url("${base}/${safeName1}.jpg")` : null,
    product2: safeName2 ? `url("${base}/${safeName2}.jpg")` : null
  };
});

// Debug watcher
watch(detailsJSON, (newValue) => {
  console.log("detailsJSON changed:", newValue);
  console.log("storeImages computed:", storeImages.value);
}, { immediate: true });

// Lifecycle
onMounted(async () => {
  try {
    // Fetch url title and decode it
    const urlId = decodeURIComponent(route.params.id);

    // Fetch store data
    const response = await fetch(mapEndpoint(`meta.json?v=${Date.now()}`));
    const meta = await response.json();
    const store = meta.features.find(store => store.properties.id === urlId);

    if (!store) {
      throw new Error(`Store with id ${urlId} not found`);
    }

    storeProperties.value = store.properties;
    // // 🐞 Debug console
    // console.log("The store's properties: ", storeProperties.value);

    // Fetch details.json after store properties are loaded
    try {
      const { id, type, title } = store.properties;
      const country = id.split('_')[0];
      const safeTitle = title
        .replace(/&/g, 'and')
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-');

      const url = `${import.meta.env.VITE_CDN_URL}/stores/${country}/${type}/${safeTitle}/details.json?v=${Date.now()}`;

      const res = await fetch(url);
      if (!res.ok) throw new Error(`Failed to load details.json: ${res.status}`);
      detailsJSON.value = await res.json();
    } catch (err) {
      console.error('❌ Failed to fetch details.json:', err);
      detailsJSON.value = null;
    }

  } catch (err) {
    console.error('Error fetching store data:', err);
    error.value = err.message;
  } finally {
    isLoading.value = false;
  }
});
</script>

<style lang="scss" scoped>
.image-loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: var(--background);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
  backdrop-filter: blur(8px);
}

.body {
  position: relative;

  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  overflow-y: auto;

  background-color: var(--background);
}

.hero-container {
  position: relative;
  width: 100%;

  // Maintains 1:1 aspect ratio
  padding-top: 100%;

  // Image setting
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;

  border-radius: 0 0 var(--round-xl) var(--round-xl);
}

// Buttons on hero image
.left-arrow,
.right-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.left-arrow {
  left: var(--block);
}

.right-arrow {
  right: var(--block);
}

.home-btn {
  position: absolute;
  left: var(--block);
  top: var(--block);
}

.share-btn {
  position: absolute;
  right: var(--block);
  top: var(--block);
}

// Store title and description
.key-info-container {
  flex-direction: column;
  gap: var(--block);
}

.store-description {
  align-items: flex-start;
  align-self: stretch;
  padding: var(--block);
  border-radius: var(--round-m);
  background: var(--content);
  color: var(--primary-content);
}

.products-shortcut {
  align-items: flex-start;
  width: 100%;
  gap: var(--block);
}

.leftImage {
  align-items: center;
  // width: 100px;
  width: 66%;
  height: 100px;
  border-radius: var(--round-l);
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.rightImage {
  align-items: center;
  // width: 100px;
  width: 34%;
  height: 100px;
  border-radius: var(--round-l); // Image setting
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.content-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  padding: var(--wrapper);
  gap: var(--container)
}

.title-block {
  align-items: flex-start;
  align-items: center;
  justify-content: flex-start;
  align-content: flex-start;
  align-self: stretch;
  gap: var(--block);
}
</style>
