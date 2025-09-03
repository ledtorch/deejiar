<template>
  <section class="auth-container">

    <div class="nav">
      <div class="brand-logo-block">
        <img src="/icon/logo/logo-app.png" class="app-logo">
        <h4>Deejiar</h4>
      </div>
      <Close @close="closeBottomSheet" />
    </div>
    <h4 class="promo-text">Map for Taste Adventurers to Explore without Boundaries</h4>
    <SocialAuthButton action="Continue with Instagram" instagram />
    <SocialAuthButton action="Continue with X" x />
    <Divider or />
    <InputMail ref="emailInputRef" v-model="emailValue" placeholder="Enter your email address" :autoFocus="true"
      @editing-start="handleEmailEditingStart" @editing-end="handleEmailEditingEnd" @submit="handleEmailSubmit" />
    <p class="consent-notice _caption2">By continuing, you agree to Deejiar’s Comsumer Terms and Usage Policy, and
      acknowledge their Privacy Policy.</p>
  </section>
</template>

<script setup>
import { ref, nextTick } from 'vue';

import Close from '../../button/Icon/Close.vue';
import Divider from '../../common/Divider.vue';
import SocialAuthButton from '../../button/CTA/SocialAuthButton.vue';
import InputMail from '../../form/InputMail.vue';
import PrimaryButton from '../../button/CTA/PrimaryButton.vue';

const emit = defineEmits(['close', 'height-change']);
const closeBottomSheet = () => {
  emit("close");
};

const panelContainer = ref(null);
const DEFAULT_HEIGHT = 396;
const MAX_HEIGHT_OFFSET = 100;

const calculateAndEmitHeight = async () => {
  await nextTick();
  await new Promise(resolve => setTimeout(resolve, 50)); // DOM rendering delay

  const measuredHeight = panelContainer.value.scrollHeight;
  const maxAllowedHeight = window.innerHeight - 100;

  let newHeight;

  if (measuredHeight <= DEFAULT_HEIGHT) {
    newHeight = `${DEFAULT_HEIGHT}px`;
  } else if (measuredHeight >= maxAllowedHeight - MAX_HEIGHT_OFFSET) {
    newHeight = `calc(100vh - env(safe-area-inset-top) - ${MAX_HEIGHT_OFFSET}px)`;
  } else {
    newHeight = `${Math.min(measuredHeight + 20, maxAllowedHeight - MAX_HEIGHT_OFFSET)}px`;
  }

  emit('height-change', newHeight);
};
</script>

<style lang="scss" scoped>
.auth-container {
  display: flex;
  flex-direction: column;
  gap: var(--block);
  // width: 100%;
  padding: 0 var(--container);
}

.nav {
  justify-content: space-between;
  align-items: center;
}

.brand-logo-block {
  align-items: center;
  gap: var(--unit);
}

.app-logo {
  width: 32px;
  height: 32px;
}

.promo-text {
  color: var(--tertiary-text);
}

.consent-notice {
  text-align: center;
  color: var(--tertiary-text);
}
</style>
