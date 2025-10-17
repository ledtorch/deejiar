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
      <!-- <SocialAuthButton action="Continue with Instagram" instagram /> -->
      <!-- <SocialAuthButton action="Continue with X" x /> -->
      <!-- <Divider or /> -->
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
      @blur="handleInputBlur" @focus="handleInputFocus" @editing-start="handleEmailEditingStart"
      @submit="handleEmailSubmit" :hasError="hasEmailError" :errorMessage="emailErrorMessage" />

    <p class="consent-notice _caption2">By continuing, you agree to Deejiar’s Comsumer
      <a href="https://landing.deejiar.com/terms-of-use" class="link-text">Terms of Use Policy</a>,
      and acknowledge their
      <a href="https://landing.deejiar.com/privacy-policy" class="link-text">Privacy Policy</a>.
    </p>

    <!-- Error Display -->
    <div v-if="generalError" class="error-message">
      {{ generalError }}
    </div>

    <template v-if="isEnteringEmail">
      <div class="button-set">
        <NeutralButton action="Back" type="icon-left" icon="arrow-left" @click="handleBack" />
        <PrimaryButton :action="buttonText" :type="isSubmitting ? 'default' : 'icon-right'"
          :icon="isSubmitting ? '' : 'arrow-right'" @click="submitEmail" :disabled="isSubmitting" />
      </div>
    </template>
  </section>
</template>

<script setup>
import { computed, ref, nextTick, watch, inject } from 'vue';
import { Keyboard } from '@capacitor/keyboard'

import Close from '../../button/Icon/Close.vue';
import Divider from '../../common/Divider.vue';
import SocialAuthButton from '../../button/CTA/SocialAuthButton.vue';
import InputMail from '../../forms/InputMail.vue';
import PrimaryButton from '../../button/CTA/PrimaryButton.vue';
import NeutralButton from '../../button/CTA/NeutralButton.vue';

const API_ENDPOINT = import.meta.env.VITE_API_URL;
const emit = defineEmits(['close', 'height-change']);
const bottomSheetControls = inject('bottomSheetControls');

// Refs
const state = ref('default');
const emailInputRef = ref(null);
const isEnteringEmail = ref(false);
const emailValue = ref('');

const hasEmailError = ref(false);
const emailErrorMessage = ref('');
const generalError = ref('');
const userAction = ref(''); // 'register' or 'login'

// Button animation
const isSubmitting = ref(false);
const loadingDots = ref('');

const buttonText = computed(() => {
  return isSubmitting.value ? `Sending${loadingDots.value}` : 'Next';
});

const startLoadingAnimation = () => {
  let dotCount = 0;
  const loadingInterval = setInterval(() => {
    dotCount = (dotCount + 1) % 4; // 0, 1, 2, 3, then repeat
    loadingDots.value = '.'.repeat(dotCount);

    // Stop animation when no longer submitting
    if (!isSubmitting.value) {
      clearInterval(loadingInterval);
      loadingDots.value = '';
    }
  }, 500); // Change dots every 500ms
};


// ------------------------------------
const closeBottomSheet = () => {
  emit("close");
};

const handleBack = () => {
  // Reset UI state
  isEnteringEmail.value = false;
  state.value = 'default';
  emailValue.value = '';
  clearErrors();

  bottomSheetControls.switchPanel('default');
};

// Email handlers
const handleEmailEditingStart = () => {
  isEnteringEmail.value = true;
  state.value = 'entering-email';
  focusEmailInput();
  clearErrors();
  // Expand to full height once user tabs the email input
  emit('height-change', `calc(100vh - env(safe-area-inset-top))`);
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
  if (isSubmitting.value) return;
  const email = emailInputRef.value?.getCurrentValue() || emailValue.value;

  // Validate email first
  if (!email || !email.includes('@')) {
    hasEmailError.value = true;
    emailErrorMessage.value = 'Please enter a valid email address';
    return;
  }

  isSubmitting.value = true;
  startLoadingAnimation(); // Start the animation

  try {
    // Your existing API calls...
    const checkResponse = await fetch(`${API_ENDPOINT}/user/auth/check-email`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });

    if (!checkResponse.ok) {
      throw new Error('Failed to check email');
    }

    const checkData = await checkResponse.json();
    userAction.value = checkData.suggested_action;

    const endpoint = userAction.value === 'login'
      ? '/user/auth/login/send-otp'
      : '/user/auth/register/send-otp';

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
      generalError.value = data.message || 'Authentication failed';
    }

  } catch (error) {
    console.error('Email submission error:', error);
    generalError.value = 'Network error. Please check your connection and try again.';
  } finally {
    isSubmitting.value = false; // This will stop the animation
  }
};

// Focus search input and show keyboard
const focusEmailInput = async () => {
  await nextTick();

  if (emailInputRef.value) {
    const inputElement = emailInputRef.value.$el.querySelector('input');
    if (inputElement) {
      inputElement.focus();
    }
  }

  try {
    await Keyboard.show();
  } catch (error) {
    console.log(error);
  }
};

watch(emailValue, (newValue) => {
  if (newValue && newValue.length > 0) {
    state.value = 'entering-email';
    isEnteringEmail.value = true;
  }
});

// Handle state change
const handleInputBlur = () => {
  if (isEnteringEmail.value) {
    state.value = 'not-entering-email';
  }
};

const handleInputFocus = () => {
  if (isEnteringEmail.value) {
    state.value = 'entering-email';
  }
};

// Adjust the sheet height on its state
watch(() => state.value, async (newState) => {
  switch (newState) {
    case 'default':
      emit('height-change', '290px');
      break;
    case 'entering-email':
      emit('height-change', 'calc(100vh - env(safe-area-inset-top))');
      break;
    case 'not-entering-email':
      emit('height-change', '388px');
      break;
  }
}, { immediate: true });
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

.link-text {
  color: var(--secondary-text);
  text-decoration: underline;
}
</style>
