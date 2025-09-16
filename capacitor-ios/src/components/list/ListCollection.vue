<template>
  <section class="list-container" @click="renderCollectionStores">
    <img :src="topicData.thumbnail" class="thumbnail">
    <div class="content">
      <p class="list-title _subtitle">{{ topicData.title }}</p>
      <p class="list-subtitle _caption1">{{ topicData.subtitle }}</p>
    </div>
    <img :src="topicData.icon" class="topic-icon">
  </section>
</template>

<script setup>
import { computed } from 'vue';
import { useMapStore } from '../../stores/mapStore.js';

const props = defineProps({
  cocktail: {
    type: Boolean,
    default: false
  },
  taco: {
    type: Boolean,
    default: false
  },
  icecream: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['render', 'select']);
const mapStore = useMapStore();

// JSON Endpoints
const mapEndpoint = (path) => {
  return `${import.meta.env.VITE_API_URL}/map/${path}`;
};

// Fixed data for MVP
const topicData = computed(() => {
  if (props.cocktail) {
    return {
      title: "Best Bars After Dark — Taipei",
      subtitle: "Sip. Savor. Stay out late.",
      thumbnail: "/icon/collection/cocktail.jpg",
      icon: "/icon/collection/cocktail.png",
      type: 'cocktail',
      url: mapEndpoint('collectionA.json'),
    };
  }

  if (props.icecream) {
    return {
      title: "Ice Cream for a Rainy Day",
      subtitle: "Sweet comfort for a cloudy mood.",
      thumbnail: "/icon/collection/icecream.jpg",
      icon: "/icon/collection/icecream.png",
      type: 'icecream',
      url: mapEndpoint('collectionB.json')
    };
  }

  if (props.taco) {
    return {
      title: "Tacos in the Alley",
      subtitle: "Hidden flavors locals swear by.",
      thumbnail: "/icon/collection/taco.jpg",
      icon: "/icon/collection/taco.png",
      type: 'taco',
      url: mapEndpoint('collectionC.json')
    };
  }

  // Default fallback
  return {
    title: "Test Title",
    subtitle: "Test Subtitle",
    thumbnail: "",
    icon: ""
  };
});

// Handle collection click - load data to map store
const renderCollectionStores = async () => {
  try {
    // Load the collection data into the map store
    await mapStore.loadCollection(topicData.value.type);

    // Emit events for other components to react
    emit('render', topicData.value.type);
    emit('select', {
      type: topicData.value.type,
      url: topicData.value.url,
      data: topicData.value
    });

    console.log(`🎯 Collection ${topicData.value.type} loaded to map`);
  } catch (error) {
    console.error(`Failed to load collection ${topicData.value.type}:`, error);
  }
};

</script>

<style lang="scss" scoped>
.list-container {
  position: relative;
  display: flex;
  padding: var(--unit);
  align-items: center;
  gap: var(--division);
  background-color: var(--gray-button);
  border-radius: var(--round-m);
  width: 100%;
  overflow: hidden;

  &:active {
    opacity: 0.7;
  }
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--atom);
  z-index: 2;
}

.list-title {
  color: var(--primary-text);
}

.list-subtitle {
  color: var(--secondary-text);
}

.thumbnail {
  width: 68px;
  height: 68px;
  border-radius: var(--round-l);
  object-fit: cover;
}

.topic-icon {
  width: 80px;
  height: 80px;
  position: absolute;
  right: -24px;
  bottom: -24px;
  object-fit: contain;
  z-index: 1;
}
</style>