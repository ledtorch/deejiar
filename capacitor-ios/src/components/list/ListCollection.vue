<template>
  <section class="list-container">
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

// Fixed data for MVP
const topicData = computed(() => {
  if (props.cocktail) {
    return {
      title: "TOP 50 Bars in Asia",
      subtitle: "Sip. Savor. Stay out late.",
      thumbnail: "/icon/collection/cocktail.jpg",
      icon: "/icon/collection/cocktail.png"
    };
  }

  if (props.taco) {
    return {
      title: "Tacos in the Alley",
      subtitle: "Hidden flavors locals swear by.",
      thumbnail: "/icon/collection/taco.jpg",
      icon: "/icon/collection/taco.png"
    };
  }

  if (props.icecream) {
    return {
      title: "Ice Cream for a Rainy Day",
      subtitle: "Sweet comfort for a cloudy mood.",
      thumbnail: "/icon/collection/icecream.jpg",
      icon: "/icon/collection/icecream.png"
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