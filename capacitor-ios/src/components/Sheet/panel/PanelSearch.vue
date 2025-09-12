<template>
  <section class="search-container">
    <div class="search-component">
      <TheSearch />
      <TheAvatar class="avatar-layout" userState="default" uphoto="..." uid="..." :useBottomSheet="true" />
    </div>
    <div class="collection-container">
      <p class="_subtitle collection-title">Deejiar Collections</p>
      <ListCollection cocktail />
      <ListCollection icecream />
      <ListCollection taco />
    </div>
    <PrimaryButton :action="CTAButtonText" type="default" @click="handleLoginOrRegister" />
  </section>
</template>

<script setup>
import TheSearch from '../../TheSearch.vue';
import TheAvatar from '../../button/TheAvatar.vue';
import PrimaryButton from '../../button/CTA/PrimaryButton.vue';
import ListCollection from '../../list/ListCollection.vue';
import { inject, computed } from 'vue';
import { useUserStore } from '../../../stores/userStore';
import { useRouter } from 'vue-router';

const router = useRouter();
const userStore = useUserStore();
const bottomSheetControls = inject('bottomSheetControls', null);

const handleLoginOrRegister = () => {
  if (userStore.userState === 'default') {
    bottomSheetControls.switchPanel('auth');
  } else if (userStore.userState === 'active') {
    router.push({ name: 'subscription' });
  }
};

const CTAButtonText = computed(() => {
  if (userStore.userState === 'default') {
    return 'Log in to Unlock Advanced Features';
  } else if (userStore.userState === 'active') {
    return 'Unlock Advanced Features';
  }
});
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