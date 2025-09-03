<template>
  <main class="body">
    <section v-if="!isSubscribed" class="main-container">
      <HeaderPage :pagetitle="'Account'" />
      <div class="account-overview">
        <TheAvatar userState="active" class="avatar-layout" />
        <img src="/icon/subscription-medal/none.svg" class="level-icon">
      </div>
      <Divider />
      <Divider or />
      <Divider vertical />
      <PrimaryButton action="Start Free Trial" default />
    </section>

    <section v-else class="main-container">
      <HeaderPage :pagetitle="'Account'" />
      <div class="account-overview">
        <TheAvatar userState="active" class="avatar-layout" />
        <img src="/icon/subscription-medal/none.svg" class="level-icon">
      </div>
      <Divider />
      <Divider or />
      <Divider vertical />
      <PrimaryButton action="Share Your Feedback" default />
    </section>
  </main>
</template>

<script setup>
import HeaderPage from '../components/nav/HeaderPage.vue'
import TheAvatar from '../components/button/TheAvatar.vue'
import Divider from '../components/common/Divider.vue'
import PrimaryButton from '../components/button/CTA/PrimaryButton.vue'
</script>

<style lang="scss" scoped>
.body {
  /* Positioning */
  position: relative;

  /* Layout */
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
</style>