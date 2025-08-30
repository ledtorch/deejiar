<template>
  <main class="body">
    <section class="main-container">
      <HeaderPage :pagetitle="'Join the Deejiar Pioneers'"></HeaderPage>
      <img :src="bannerImage" alt="">
      <div class="promote-feature-container">
        <TheAvatar userState="active" class="avatar-in-subscription" />
        <img src="/icon/action/arrow-right.svg" class="arrow-right-in-subscription">
        <TheAvatar userState="premium" class="avatar-in-subscription" />
      </div>
      <SubscriptionRadioCard />
    </section>
    <PrimaryButton action="Start Free Trial" />
  </main>
</template>

<script setup>
import HeaderPage from '../components/nav/HeaderPage.vue'
import PrimaryButton from '../components/button/CTA/PrimaryButton.vue'
import bannerImage from '@/assets/images/lv1-banner.svg'
import TheAvatar from '../components/button/TheAvatar.vue'
import SubscriptionRadioCard from '../components/card/SubscriptionRadioCard.vue'
</script>

<style lang="scss" scoped>
.body {
  /* Positioning */
  position: relative;

  /* Layout & Box Model */
  display: flex;
  flex-direction: column;
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
  justify-content: space-between;
  align-items: center;
  gap: var(--division);
}

.promote-feature-container {
  align-items: center;
  gap: var(--block);
}

.avatar-in-subscription {
  width: 44px;
  height: 44px;
}

.arrow-right-in-subscription {
  width: 24px;
  height: 24px;
}
</style>