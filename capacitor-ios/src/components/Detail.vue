<template>
  <div class="body flex-col">
    <!-- Carousel Content -->
    <div v-if="currentPage === 0" class="cover" :style="{ 'backgroundImage': storeFrontImage }">
      <LeftArrow @click="previousPage" class="left-arrow" />
      <Home @click="toHomePage" class="home-btn" />
      <Share @click="share" class="share-btn" />
      <RightArrow @click="nextPage" class="right-arrow" />
    </div>
    <div v-else class="cover" :style="{ 'backgroundImage': currentItem }">
      <LeftArrow @click="previousPage" class="left-arrow" />
      <HomeToDetail @click="toDetailHomePage" class="home-btn" />
      <RightArrow @click="nextPage" class="right-arrow" />
    </div>

    <!-- Cover Page -->
    <div v-if="currentPage === 0" class="content flex-col">
      <!-- Loading state -->
      <div v-if="isLoading" class="content-frame">
        <p>Loading store information...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="content-frame">
        <p>Error: {{ error }}</p>
      </div>

      <!-- Store data loaded -->
      <div v-else-if="storeProperties" class="content-frame">
        <div class="items-frame">
          <div class="leftImage" :style="{ 'backgroundImage': storeImages.product1 }"></div>
          <div class="rightImage" :style="{ 'backgroundImage': storeImages.product2 }"></div>
        </div>
        <div class="content-frame">
          <div class="title-block">
            <h4 class="_stretch">{{ storeProperties.title }}</h4>
            <TagShopType :store="storeProperties" />
          </div>
          <p class="frame-intro">{{ detailsJSON.description }}</p>
        </div>
        <Businesshour :bizTime="detailsJSON.businesshour" viewMode="overview" />
        <div class="splitline"></div>
        <div class="content-frame">
          <!-- <Businesshour :bizTime="detailsJSON.businesshour" viewMode="detail" /> -->
        </div>
        <div class="content-frame">
          <Address :address="detailsJSON.address" />
        </div>
        <div class="splitline"></div>
        <GetDirection variant="apple" :appleAUID="storeProperties.auid"></GetDirection>
        <GetDirection variant="google" :storeTitle="storeProperties.title"></GetDirection>
        <!-- // 🏗️ TODO -->
        <!-- <GetDirection variant="google" :googlePlaceid="googlePlaceid"></GetDirection> -->
      </div>
    </div>

    <!-- Product Page -->
    <div v-else class="content flex-col">
      <div v-if="currentProduct" class="title-block">
        <h4 class="_stretch">{{ currentProduct.name }}</h4>
        <h4>{{ currentProduct.price }}</h4>
      </div>
      <!-- Use v-html to render <br> -->
      <p v-if="currentProduct" class="frame-intro" v-html="currentProduct.description"></p>
      <!-- <GetDirection variant="apple" :appleAUID="appleAUID"></GetDirection>
      <GetDirection variant="google" :storeTitle="storeTitle"></GetDirection> -->
      <!-- // 🏗️ TODO -->
      <!-- <GetDirection variant="google" :googlePlaceid="googlePlaceid", ></GetDirection> -->
    </div>

  </div>
</template>

<script setup>
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
  router.push('/');
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

// Default share function
// const share = () => {
//   if (navigator.share) {
//     navigator.share({
//       title: storeTitle.value,
//       text: `Check out ${storeTitle.value} with Deejiar!`,
//       url: window.location.href
//     }).then(() => {
//       console.log('Successfully shared');
//     }).catch((error) => {
//       console.error('Error sharing:', error);
//     });
//   } else {
//     alert('Sharing is not supported on this browser');
//   }
// };


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
// Frame
.body {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow-y: auto;

  /* 📱 Account for top safe area */
  top: env(safe-area-inset-top);

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
  align-items: center;
  justify-content: flex-start;
  align-content: flex-start;
  align-self: stretch;
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

.content-frame {
  flex-direction: column;
  gap: 12px;
}

.items-frame {
  align-items: flex-start;
  width: 100%;
  gap: 12px;
}

.frame-intro {
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
