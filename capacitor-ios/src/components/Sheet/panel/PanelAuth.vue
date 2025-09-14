<template>
  <section class="auth-container">
    <template v-if="!isEnteringEmail">
      <div class="nav">
        <div class="brand-logo-block">
          <img src="/icon/logo/logo-app.png" class="app-logo">
          <h4>Deejiar</h4>
        </div>
        <Close type="modal" @close="closeBottomSheet" />
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
      @editing-start="handleEmailEditingStart" @editing-end="handleEmailEditingEnd" @submit="handleEmailSubmit"
      :hasError="hasEmailError" :errorMessage="emailErrorMessage" />

    <p class="consent-notice _caption2">By continuing, you agree to Deejiar’s Comsumer
      <a href="https://github.com/ledtorch/deejiar/blob/main/capacitor-ios/terms-and-usage-policy.md">Terms and Usage
        Policy</a>,
      and acknowledge their
      <a href="https://github.com/ledtorch/deejiar/blob/main/capacitor-ios/privacy-policy.md">Privacy Policy</a>.
    </p>

    <!-- Error Display -->
    <div v-if="generalError" class="error-message">
      {{ generalError }}
    </div>

    <template v-if="isEnteringEmail">
      <div class="button-set">
        <NeutralButton action="Back" type="icon-left" icon="arrow-left" @click="handleBack" />
        <PrimaryButton action="Next" type="icon-right" icon="arrow-right" @click="submitEmail" />
      </div>
    </template>
  </section>
</template>

<script setup>
import { ref, nextTick, watch, inject } from 'vue';

import Close from '../../button/Icon/Close.vue';
import Divider from '../../common/Divider.vue';
import SocialAuthButton from '../../button/CTA/SocialAuthButton.vue';
import InputMail from '../../form/InputMail.vue';
import PrimaryButton from '../../button/CTA/PrimaryButton.vue';
import NeutralButton from '../../button/CTA/NeutralButton.vue';

const emit = defineEmits(['close', 'height-change']);
const bottomSheetControls = inject('bottomSheetControls');

// Refs
const panelContainer = ref(null);
const DEFAULT_HEIGHT = 396;
const MAX_HEIGHT_OFFSET = 100;

const emailInputRef = ref(null);
const isEnteringEmail = ref(false);
const emailValue = ref('');

const hasEmailError = ref(false);
const emailErrorMessage = ref('');
const generalError = ref('');
const userAction = ref(''); // 'register' or 'login'

const API_ENDPOINT = import.meta.env.VITE_API_URL;


const closeBottomSheet = () => {
  emit("close");
};


// Email handlers
const handleEmailEditingStart = () => {
  isEnteringEmail.value = true;
  clearErrors();
  // Expand to full height once user tabs the email input
  emit('height-change', `calc(100vh - env(safe-area-inset-top))`);
};

const handleEmailEditingEnd = () => {
  // Keep expanded if email has value
  if (emailValue.value) {
  } else {
    isEnteringEmail.value = false;
    emit('height-change', '450px');
  }
};

const handleBack = () => {
  isEnteringEmail.value = false;
  emailValue.value = '';
  clearErrors();
  emit('height-change', '450px');
};

const handleEmailSubmit = () => {
  submitEmail();
};

const clearErrors = () => {
  hasEmailError.value = false;
  emailErrorMessage.value = '';
  generalError.value = '';
};

const submitEmail = async () => {
  const email = emailInputRef.value?.getCurrentValue() || emailValue.value;

  // Validate email first
  if (!email || !email.includes('@')) {
    hasEmailError.value = true;
    emailErrorMessage.value = 'Please enter a valid email address';
    return;
  }

  try {
    // Check if user exists first
    const checkResponse = await fetch(`${API_ENDPOINT}/api/user/auth/check-email`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });

    if (!checkResponse.ok) {
      throw new Error('Failed to check email');
    }

    const checkData = await checkResponse.json();
    userAction.value = checkData.suggested_action;

    // Send appropriate OTP based on user existence
    const endpoint = userAction.value === 'login'
      ? '/api/user/auth/login/send-otp'
      : '/api/user/auth/register/send-otp';

    const response = await fetch(`${API_ENDPOINT}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });

    const data = await response.json();

    if (response.ok) {
      bottomSheetControls.switchPanel('authOTP', {
        email: email,
        action: userAction.value
      });
    } else {
      // Handle API errors
      handleEmailSubmissionError(response.status, data);
    }

  } catch (error) {
    console.error('Email submission error:', error);
    generalError.value = 'Network error. Please check your connection and try again.';
  }
};

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

</script>

<style lang="scss" scoped>
.auth-container {
  display: flex;
  flex-direction: column;
  gap: var(--block);
  padding: var(--container) var(--wrapper) 0 var(--wrapper);
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
