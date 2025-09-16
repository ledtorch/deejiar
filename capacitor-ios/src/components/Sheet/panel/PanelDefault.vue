<template>
  <section class="search-container">
    <!-- Filter Tag - Show when collection is active -->
    <div v-if="showFilterTag" class="filter-tag-container">
      <TagFilter :icon="currentFilterTag.icon" :text="currentFilterTag.text" @close="resetToAllStores" />
    </div>

    <div class="search-component">
      <TheSearch @click="handleSearch" />
      <TheAvatar class="avatar-layout" userState="default" uphoto="..." uid="..." :useBottomSheet="true" />
    </div>

    <div class="collection-container">
      <p class="_subtitle collection-title">Deejiar Collections</p>
      <ListCollection cocktail @render="handleCollectionRender" />
      <ListCollection icecream @render="handleCollectionRender" />
      <ListCollection taco @render="handleCollectionRender" />
    </div>

    <PrimaryButton :action="CTAButtonText" type="default" @click="handleLoginOrRegister" />
  </section>
</template>

<script setup>
import { inject, computed, ref, watch } from 'vue';
import { useUserStore } from '../../../stores/userStore';
import { useMapStore } from '../../../stores/mapStore';
import { useRouter } from 'vue-router';
import TheSearch from '../../TheSearch.vue';
import TheAvatar from '../../button/TheAvatar.vue';
import PrimaryButton from '../../button/CTA/PrimaryButton.vue';
import ListCollection from '../../list/ListCollection.vue';
import TagFilter from '../../button/tag/TagFilter.vue';

const router = useRouter();
const userStore = useUserStore();
const mapStore = useMapStore();
const bottomSheetControls = inject('bottomSheetControls', null);

// Filter tag state
const activeCollection = ref(null);

// // Computed properties
// const showFilterTag = computed(() => {
//   return activeCollection.value !== null;
// });

const showFilterTag = ref(false);

const currentFilterTag = computed(() => {
  const collectionTags = {
    cocktail: { icon: 'cocktail', text: 'Best Bars After Dark — Taipei' },
    icecream: { icon: 'icecream', text: 'Ice Cream for a Rainy Day' },
    taco: { icon: 'taco', text: 'Tacos in the Alley' }
  };

  return collectionTags[activeCollection.value] || { icon: '', text: '' };
});

const CTAButtonText = computed(() => {
  if (userStore.userState === 'default') {
    return 'Log in to Unlock Advanced Features';
  } else if (userStore.userState === 'active') {
    return 'Unlock Advanced Features';
  }
});


// Only clear activeCollection when TagFilter close button is clicked
const resetToAllStores = () => {
  activeCollection.value = null;
  console.log('UI reset to show all stores');
};

// Methods
const handleLoginOrRegister = () => {
  if (userStore.userState === 'default') {
    bottomSheetControls.switchPanel('auth');
  } else if (userStore.userState === 'active') {
    router.push({ name: 'subscription' });
  }
};

const handleSearch = () => {
  bottomSheetControls.switchPanel('search');
};

const handleCollectionRender = (collectionType) => {
  showFilterTag.value = true;
  activeCollection.value = collectionType;
  console.log(`Collection ${collectionType} is now active`);
};

</script>

<style lang="scss" scoped>
.search-container {
  display: flex;
  flex-direction: column;
  padding: 0 var(--wrapper);
}

.search-component {
  justify-content: space-between;
  gap: var(--block);
}

.avatar-layout {
  width: 36px;
  height: 36px;
}

.collection-container {
  flex-direction: column;
  gap: var(--box);
  padding: var(--block) 0 var(--wrapper) 0;
}

.collection-title {
  color: var(--tertiary-text);
}

.filter-tag-container {
  position: fixed;
  top: calc(var(--wrapper) + env(safe-area-inset-top));
  left: 0;
  right: 0;
  z-index: 2;

  display: flex;
  justify-content: center;
  padding: var(--block) 0 0 0;

  /* Make only the TagFilter clickable */
  :deep(.tag-filter) {
    pointer-events: auto;
  }
}
</style>