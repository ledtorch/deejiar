<template>
  <section class="auth-container">
    <template v-if="!isEnteringEmail">
      <div class="nav">
        <div class="brand-logo-block">
          <img src="/icon/logo/logo-app.png" class="app-logo">
          <h4>Deejiar</h4>
        </div>
        <Close @close="closeBottomSheet" />
      </div>
      <h4 class="auth-tagline">Map for Taste Adventurers to Explore without Boundaries</h4>
      <SocialAuthButton action="Continue with Instagram" instagram />
      <SocialAuthButton action="Continue with X" x />
      <Divider or />
    </template>

    <template v-if="isEnteringEmail">
      <div class="mail-input-container">
        <div class="brand-logo-block">
          <img src="/icon/logo/logo-app.png" class="app-logo">
          <h4>Deejiar</h4>
        </div>
        <h4 class="auth-email-heading">Register your account with your email address</h4>
      </div>
    </template>

    <InputMail ref="emailInputRef" v-model="emailValue" placeholder="Enter your email address" :autoFocus="true"
      @editing-start="handleEmailEditingStart" @editing-end="handleEmailEditingEnd" @submit="handleEmailSubmit" />
    <p class="consent-notice _caption2">By continuing, you agree to Deejiar’s Comsumer Terms and Usage Policy, and
      acknowledge their Privacy Policy.</p>

    <template v-if="isEnteringEmail">
      <div class="button-set">
        <NeutralButton action="Back" type="icon-left" icon="arrow-left" @click="handleBack" />
        <PrimaryButton action="Next" type="icon-right" icon="arrow-right" @click="handleNext" />
      </div>
    </template>

  </section>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue';

import Close from '../../button/Icon/Close.vue';
import Divider from '../../common/Divider.vue';
import SocialAuthButton from '../../button/CTA/SocialAuthButton.vue';
import InputMail from '../../form/InputMail.vue';
import PrimaryButton from '../../button/CTA/PrimaryButton.vue';
import NeutralButton from '../../button/CTA/NeutralButton.vue';

const emit = defineEmits(['close', 'height-change']);
const closeBottomSheet = () => {
  emit("close");
};

const panelContainer = ref(null);
const DEFAULT_HEIGHT = 396;
const MAX_HEIGHT_OFFSET = 100;

const isEnteringEmail = ref(false);
const emailValue = ref('');

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

// Watch email value to determine if user is entering email
watch(emailValue, (newValue) => {
  if (newValue && newValue.length > 0) {
    isEnteringEmail.value = true;
  }
});

// Email handlers
const handleEmailEditingStart = () => {
  isEnteringEmail.value = true;
  // Expand to full height for keyboard
  // emit('height-change', `calc(100vh - env(safe-area-inset-top))`);
  emit('height-change', '354px');
};

const handleEmailEditingEnd = () => {
  // Keep expanded if email has value
  if (emailValue.value) {
    emit('height-change', `calc(100vh - env(safe-area-inset-top))`);
  } else {
    isEnteringEmail.value = false;
    emit('height-change', '450px');
  }
};

const handleBack = () => {
  isEnteringEmail.value = false;
  emit('height-change', '450px');
};

const handleNext = () => {
  isEnteringEmail.value = true;
  emit('height-change', '354px');
};
</script>

<style lang="scss" scoped>
.auth-container {
  display: flex;
  flex-direction: column;
  gap: var(--block);
  padding: var(--container) var(--container) 0 var(--container);
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

.auth-tagline {
  color: var(--tertiary-text);
}

.auth-email-heading {
  text-align: center;
  color: var(--tertiary-text);
}

.consent-notice {
  text-align: center;
  color: var(--tertiary-text);
}

.mail-input-container {
  flex-direction: column;
  align-items: center;
  padding-bottom: var(--block);
  gap: var(--block);
}

.button-set {
  width: 100%;
  padding-top: var(--wrapper);
  justify-content: space-between;
}
</style>
