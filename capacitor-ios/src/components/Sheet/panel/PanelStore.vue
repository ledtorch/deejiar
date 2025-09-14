<template>
  <section class="panel-store">
    <!-- Food Layout -->
    <template v-if="storeLayout === 'food'">
      <nav class="store-nav">
        <HeaderStore :store="store" />
        <Close type="modal" @close="handleClose" />
      </nav>

      <div class="image-gallery">
        <div class="main-image" :style="{ backgroundImage: storeImages.storefront }"></div>
        <div class="secondary-images">
          <div class="product-image" :style="{ backgroundImage: storeImages.product1 }"></div>
          <div class="product-image" :style="{ backgroundImage: storeImages.product2 }"></div>
        </div>
      </div>

      <div class="store-description">
        <p class="text-limited">
          {{ storeDetails?.description || "No description available" }}
        </p>
      </div>

      <Businesshour v-if="storeDetails?.businesshour" :bizTime="storeDetails.businesshour" viewMode="overview" />
    </template>

    <!-- View Layout -->
    <template v-else-if="storeLayout === 'view'">
      <nav class="store-nav">
        <HeaderStore :store="store" />
        <Close type="modal" @close="handleClose" />
      </nav>

      <div class="image-gallery-view">
        <div class="hero-image" :style="{ backgroundImage: storeImages.storefront }"></div>
      </div>

      <div class="store-description">
        <p class="text-limited">
          {{ storeDetails?.description || "No description available" }}
        </p>
      </div>

      <Businesshour v-if="storeDetails?.businesshour" :bizTime="storeDetails.businesshour" viewMode="overview" />
    </template>
  </section>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import HeaderStore from '../../nav/HeaderStore.vue';
import Close from '../../button/Icon/Close.vue';
import Businesshour from '../Businesshour.vue';

// Props
const props = defineProps({
  store: {
    type: Object,
    required: true
  },
  isActive: {
    type: Boolean,
    default: false
  }
});

// Emits
const emit = defineEmits(['close', 'height-change', 'navigate']);

// Store details state
const storeDetails = ref(null);
const isLoading = ref(false);
const error = ref(null);

// Computed properties
const storeLayout = computed(() => props.store?.layout || 'food');

// Generate store details endpoint
const getStoreDetailsEndpoint = () => {
  if (!props.store) return null;

  const { id, type, title } = props.store;
  const country = id.split('_')[0];
  const safeTitle = title
    .replace(/&/g, 'and')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-');

  return `${import.meta.env.VITE_CDN_URL}/stores/${country}/${type}/${safeTitle}`;
};

// Compute store images
const storeImages = computed(() => {
  const base = getStoreDetailsEndpoint();
  if (!base) return {};

  const safeProductName = (product) => {
    if (!product?.name) return null;
    return product.name
      .replace(/&/g, 'and')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/\s+/g, '-');
  };

  const product1Name = safeProductName(storeDetails.value?.product1);
  const product2Name = safeProductName(storeDetails.value?.product2);

  return {
    storefront: `url("${base}/storefront-day.jpg")`,
    product1: product1Name ? `url("${base}/${product1Name}.jpg")` : null,
    product2: product2Name ? `url("${base}/${product2Name}.jpg")` : null
  };
});

// Fetch store details
const fetchStoreDetails = async () => {
  if (!props.store) return;

  isLoading.value = true;
  error.value = null;

  try {
    const endpoint = getStoreDetailsEndpoint();
    if (!endpoint) throw new Error('Invalid store data');

    const url = `${endpoint}/details.json?v=${Date.now()}`;
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Failed to load details: ${response.status}`);
    }

    storeDetails.value = await response.json();
  } catch (err) {
    console.error('Failed to fetch store details:', err);
    error.value = err.message;
    storeDetails.value = null;
  } finally {
    isLoading.value = false;
  }
};

// Watch for store changes
watch(() => props.store, (newStore) => {
  if (newStore) {
    fetchStoreDetails();
    // Emit height change for appropriate layout
    const height = storeLayout.value === 'view' ? '500px' : '467px';
    emit('height-change', height);
  }
}, { immediate: true });

// Event handlers
const handleClose = () => {
  emit('close');
};

// Initial mount
onMounted(() => {
  if (props.store) {
    fetchStoreDetails();
  }
});
</script>

<style lang="scss" scoped>
.panel-store {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0 16px 16px;
  flex: 1;
}

.store-nav {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.image-gallery {
  display: flex;
  gap: 8px;
  align-self: stretch;

  .main-image {
    width: 180px;
    height: 180px;
    border-radius: 12px;
    background-position: center;
    background-size: cover;
    background-repeat: no-repeat;
    flex-shrink: 0;
  }

  .secondary-images {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;

    .product-image {
      height: 86px;
      border-radius: 12px;
      background-position: center;
      background-size: cover;
      background-repeat: no-repeat;
    }
  }
}

.image-gallery-view {
  .hero-image {
    width: 100%;
    height: 260px;
    border-radius: 12px;
    background-position: center;
    background-size: cover;
    background-repeat: no-repeat;
  }
}

.store-description {
  padding: 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.07);

  .text-limited {
    max-height: 48px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    text-overflow: ellipsis;
    margin: 0;
  }
}
</style>