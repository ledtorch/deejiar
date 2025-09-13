<template>
  <div class="thumbnail-frame flex-col" :style="backgroundStyle">
    <div class="base">
      <!-- <p class="_caption2">No.{{ ranking }}</p> -->
    </div>
    <div class="base">
      <p class="_caption1">{{ title }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';

const props = defineProps({
  bar: {
    type: Object,
    required: true
  }
});

const detailsJSON = ref(null);
const ranking = props.bar.properties.id;
const title = props.bar.properties.title;

// Store Details Endpoint function (same as Detail.vue)
const storeDetailsEndpoint = () => {
  if (!props.bar?.properties) return '';
  const { id, type, title } = props.bar.properties;
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

// Generate product image using the same logic as Detail.vue
const generateProductImage = computed(() => {
  if (!detailsJSON.value || !props.bar?.properties) return null;

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

  return safeName1 ? `url("${base}/${safeName1}.jpg")` : `url("${base}/storefront-day.jpg")`;
});

const backgroundStyle = computed(() => {
  return {
    backgroundImage: generateProductImage.value || 'none',
    backgroundSize: 'cover',
    backgroundPosition: 'center'
  };
});

// Fetch details.json for this bar (same logic as Detail.vue)
onMounted(async () => {
  try {
    const { id, type, title } = props.bar.properties;
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
    if (res.ok) {
      detailsJSON.value = await res.json();
    } else {
      console.warn(`Failed to load details.json for ${title}`);
      // Fallback to storefront image
      detailsJSON.value = null;
    }
  } catch (err) {
    console.error('Error fetching details.json:', err);
    detailsJSON.value = null;
  }
});
</script>

<style lang="scss" scoped>
.thumbnail-frame {
  min-width: 120px;
  min-height: 120px;

  padding: 4px;
  border-radius: 8px;
  background: lightgray 50%;

  justify-content: space-between;
  align-items: flex-start;
}

.minimize-button {
  position: absolute;
  top: 12px;
  right: 12px;
}

.base {
  padding: var(--Atom, 2px) var(--Unit, 4px);
  flex-direction: column;
  align-items: flex-start;
  border-radius: var(--Round-Mini, 4px);
  background: var(--Base-Invert-base, rgba(0, 0, 0, 0.60));
}
</style>