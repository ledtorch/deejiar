<template>
  <section class="search-container">
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

    <PrimaryButton v-if="!userStore.isPremium" :action="CTAButtonText" type="default" @click="handleLoginOrRegister" />
  </section>
</template>

<script setup>
import { inject, computed } from 'vue';
import { useUserStore } from '@/stores/userStore';
import { useRouter } from 'vue-router';
import TheSearch from '../../forms/TheSearch.vue';
import TheAvatar from '../../button/TheAvatar.vue';
import PrimaryButton from '../../button/CTA/PrimaryButton.vue';
import ListCollection from '../../list/ListCollection.vue';

const router = useRouter();
const userStore = useUserStore();
const bottomSheetControls = inject('bottomSheetControls', null);

// Emits for parent component
const emit = defineEmits(['show-tag-filter', 'height-change']);

const handleCollectionRender = (collectionType) => {
  // Emit to BottomSheet to show TagFilt
  emit('show-tag-filter', { type: collectionType });
  emit('height-change', '32px');
  console.log(`Collection ${collectionType} is now active`);
};

/* Switch panel */
const CTAButtonText = computed(() => {
  if (userStore.userState === 'default') {
    return 'Log in to Unlock Advanced Features';
  } else if (userStore.userState === 'active') {
    return 'Unlock Advanced Features';
  }
});

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
</style>