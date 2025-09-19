<template>
  <main class="page">
    <section v-if="!isSubscribed" class="main-container">
      <div class="upper-container">
        <HeaderPage :pagetitle="'Account'" />

        <div class="account-overview">
          <div class="user-info-container">
            <TheAvatar userState="active" class="avatar-layout" />
            <div class="user-info-box">
              <p class="uid _title">{{ displayName }}</p>
              <p class="subscribe-promo-button _title">Join Deejiar Pioneers?</p>
            </div>
          </div>
          <img :src="MedalIconLevel0" class="level-icon">
        </div>
        <Divider />
        <!-- For MVP -->
        <div class="page-buttons">
          <PageButton action="Mail Us" mailUs @click="mailToDeejiar" />
          <PageButton action="Follow on X" followOnX @click="openX" />
        </div>
        <!--  
        <div class="page-buttons">
          <PageButton action="Inbox" inbox />
          <PageButton action="Map" map />
          <PageButton action="Help" help />
        </div>
        -->
        <ListAccountData email />
        <!-- <ListAccountData x /> -->
        <!-- <ListAccountData instagram /> -->
        <p class="version-text _caption2">v0.01.1 Release 2025.09.09</p>
      </div>

      <div class="button-set">
        <NeutralButton action="Log Out" default @click="handleLogout" />
        <PrimaryButton action="Start Free Trial" default @click="handleStartTrial" />
      </div>
    </section>

    <section v-else class="main-container">
      <HeaderPage :pagetitle="'Account'" />
      <div class="account-overview">
        <TheAvatar userState="active" class="avatar-layout" />
        <img :src="MedalIconLevel0" class="level-icon">
      </div>
      <Divider />
      <Divider or />
      <Divider vertical />
      <PrimaryButton action="Share Your Feedback" default />
    </section>
  </main>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/userStore';
import HeaderPage from '../components/nav/HeaderPage.vue'
import TheAvatar from '../components/button/TheAvatar.vue'
import Divider from '../components/common/Divider.vue'
import PrimaryButton from '../components/button/CTA/PrimaryButton.vue'
import NeutralButton from '../components/button/CTA/NeutralButton.vue'
import ListAccountData from '../components/list/ListAccountData.vue'
import PageButton from '../components/button/PageButton.vue'

import MedalIconLevel0 from '@/assets/icons/subscription-medal/none.svg';



const router = useRouter();

const userStore = useUserStore();
const API_ENDPOINT = import.meta.env.VITE_API_URL;

const handleLogout = async () => {
  try {
    // Get the current access token
    const token = userStore.accessToken;

    if (token) {
      // Call the logout API endpoint
      await fetch(`${API_ENDPOINT}/api/user/auth/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        }
      });
    }

    // Clear user data from store (regardless of API call success)
    await userStore.logout();

    // Navigate to map
    router.push('/map');

  } catch (error) {
    console.error('Logout error:', error);

    // Even if API call fails, clear local data and redirect
    await userStore.logout();
    router.push('/map');
  }
};

const handleStartTrial = () => {
  router.push('/subscription');
};

const displayName = computed(() =>
  userStore.email?.split('@')[0] ||
  'Mx. Wanderer'
);

const mailToDeejiar = () => {
  window.open('mailto:hi@deejiar.com');
};

const openX = () => {
  window.open('https://x.com/deejiar');
};
</script>

<style lang="scss" scoped>
.page {
  /* Positioning */
  position: relative;
  /* Layout */
  display: flex;
  flex-direction: column;
  min-width: 100%;
  justify-content: space-between;
  width: 100vw;
  height: 100vh;
  padding: var(--safe-area-top) var(--wrapper) env(safe-area-inset-bottom) var(--wrapper);

  /* Visual & Colors */
  background-color: var(--background);
}

.main-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--division);
}

.main-container> :first-child {
  flex: 1;
}

.main-container> :last-child {
  flex: 0 0 auto;
}

.upper-container {
  flex-direction: column;
  width: 100%;
  gap: var(--division);
}

.user-info-container {
  align-items: center;
  gap: var(--block);
}

.user-info-box {
  flex-direction: column;
  height: auto;
  gap: var(--atom);
}

.uid {
  color: var(--primary-text);
}

.subscribe-promo-button {
  color: var(--color-green);
}

.account-overview {
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}

.level-icon {
  width: 60px;
  height: 60px;
}

.avatar-layout {
  width: 60px;
  height: 60px;
}

.account-section {
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}

.version-text {
  color: var(--tertiary-text);
}

.button-set {
  gap: var(--block);
  width: 100%;
}

.button-set> :first-child {
  flex: 0 0 auto;
}

.button-set> :last-child {
  flex: 1;
}

.page-buttons {
  gap: var(--block);
  width: 100%;
}
</style>