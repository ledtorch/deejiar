<template>
  <section class="auth-container" ref="panelContainer">
    <div class="otp-content">
      <!-- Email Icon Illustration -->
      <img src="/illustration/inbox.png" class="inbox-icon">

      <!-- Heading and Email Display -->
      <div class="otp-header">
        <h4 class="auth-otp-heading">Check your mailbox to finish signing in</h4>
        <p class="email-display">
          We sent your code to<br>
          <strong>{{ userEmail }}</strong>
        </p>
      </div>

      <!-- 6-Digit Code Input -->
      <div class="code-input-section">
        <InputCode ref="codeInputRef" v-model="otpCode" :autoFocus="true" :hasError="hasCodeError"
          :errorMessage="codeErrorMessage" @complete="handleCodeComplete" @editing-start="handleCodeEditingStart"
          @editing-end="handleCodeEditingEnd" />
      </div>

      <!-- Resend Option -->
      <div class="resend-section">
        <button class="resend-link" @click="resendCode" :disabled="resendCooldown > 0 || isResending">
          <template v-if="resendCooldown > 0">
            Resend code in {{ resendCooldown }}s
          </template>
          <template v-else-if="isResending">
            Sending...
          </template>
          <template v-else>
            Didn't receive a code?
          </template>
        </button>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="button-set">
      <NeutralButton action="Back" type="icon-left" icon="arrow-left" @click="handleBack" />
      <PrimaryButton action="Verify" type="icon-right" icon="arrow-right" @click="submitCode" :loading="isVerifying"
        :disabled="!isCodeComplete" />
    </div>

    <!-- Error Display -->
    <div v-if="generalError" class="error-banner">
      {{ generalError }}
    </div>
  </section>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue';

import InputCode from '../../form/InputCode.vue';
import PrimaryButton from '../../button/CTA/PrimaryButton.vue';
import NeutralButton from '../../button/CTA/NeutralButton.vue';

const props = defineProps({
  email: {
    type: String,
    required: true
  },
  action: {
    type: String,
    default: 'register' // 'register' or 'login'
  }
});

const emit = defineEmits(['close', 'height-change', 'back-to-email', 'auth-success']);

// Refs
const panelContainer = ref(null);
const codeInputRef = ref(null);

// State
const otpCode = ref('');
const userEmail = ref(props.email);
const isVerifying = ref(false);
const isResending = ref(false);
const hasCodeError = ref(false);
const codeErrorMessage = ref('');
const generalError = ref('');
const resendCooldown = ref(0);

// API endpoint
const API_ENDPOINT = import.meta.env.VITE_API_URL;

// Computed
const isCodeComplete = computed(() => {
  return otpCode.value.length === 6;
});

// Height management
const DEFAULT_HEIGHT = 420;
const MAX_HEIGHT_OFFSET = 100;

const calculateAndEmitHeight = async () => {
  await nextTick();
  await new Promise(resolve => setTimeout(resolve, 50));

  const measuredHeight = panelContainer.value?.scrollHeight || DEFAULT_HEIGHT;
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

// Event handlers
const handleCodeEditingStart = () => {
  clearErrors();
  emit('height-change', '380px'); // Compact height for keyboard
};

const handleCodeEditingEnd = () => {
  emit('height-change', `${DEFAULT_HEIGHT}px`);
};

const handleCodeComplete = (code) => {
  if (code.length === 6) {
    // Auto-submit when code is complete
    submitCode();
  }
};

const handleBack = () => {
  emit('back-to-email');
};

const clearErrors = () => {
  hasCodeError.value = false;
  codeErrorMessage.value = '';
  generalError.value = '';
};

const submitCode = async () => {
  const code = codeInputRef.value?.getCurrentValue() || otpCode.value;

  if (!code || code.length !== 6) {
    hasCodeError.value = true;
    codeErrorMessage.value = 'Please enter the 6-digit code';
    return;
  }

  isVerifying.value = true;
  clearErrors();

  try {
    // Determine endpoint based on action
    const endpoint = props.action === 'login'
      ? '/api/user/auth/login/verify-otp'
      : '/api/user/auth/register/verify-otp';

    const response = await fetch(`${API_ENDPOINT}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: userEmail.value,
        otp: code
      })
    });

    const data = await response.json();

    if (response.ok) {
      // Store authentication tokens
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      localStorage.setItem('user', JSON.stringify(data.user));

      // Emit success event
      emit('auth-success', data.user);

      // Close the panel or navigate
      emit('close');

      console.log('Authentication successful:', data.user);
    } else {
      // Handle different error types
      if (response.status === 401) {
        hasCodeError.value = true;
        codeErrorMessage.value = 'Invalid or expired code';
        // Clear the input for retry
        codeInputRef.value?.clear();
      } else {
        generalError.value = data.detail || 'Verification failed. Please try again.';
      }
    }

  } catch (error) {
    console.error('OTP verification error:', error);
    generalError.value = 'Network error. Please check your connection and try again.';
  } finally {
    isVerifying.value = false;
  }
};

const resendCode = async () => {
  if (resendCooldown.value > 0 || isResending.value) return;

  isResending.value = true;
  clearErrors();

  try {
    // Determine endpoint based on action
    const endpoint = props.action === 'login'
      ? '/api/user/auth/login/send-otp'
      : '/api/user/auth/register/send-otp';

    const response = await fetch(`${API_ENDPOINT}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: userEmail.value })
    });

    const data = await response.json();

    if (response.ok) {
      // Start cooldown
      startResendCooldown();

      // Clear current code and focus input
      codeInputRef.value?.clear();

      console.log('OTP resent successfully');
    } else {
      generalError.value = data.detail || 'Failed to resend code. Please try again.';
    }

  } catch (error) {
    console.error('Resend OTP error:', error);
    generalError.value = 'Network error. Please try again.';
  } finally {
    isResending.value = false;
  }
};

const startResendCooldown = () => {
  resendCooldown.value = 60; // 60 seconds
  const interval = setInterval(() => {
    resendCooldown.value--;
    if (resendCooldown.value <= 0) {
      clearInterval(interval);
    }
  }, 1000);
};

// Lifecycle
onMounted(() => {
  calculateAndEmitHeight();
  startResendCooldown(); // Start initial cooldown
});

onUnmounted(() => {
  // Clean up any intervals if component is destroyed
});

// Expose methods for parent component
defineExpose({
  clearErrors,
  focusInput: () => codeInputRef.value?.focus()
});
</script>

<style lang="scss" scoped>
.auth-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: var(--block);
  padding: var(--container) var(--container) 0 var(--container);
  min-height: 380px;
}

.otp-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--block);
  flex: 1;
}

.inbox-icon {
  width: 120px;
  height: 120px;
}

.otp-header {
  text-align: center;
  max-width: 280px;
}

.auth-otp-heading {
  color: var(--primary-text);
  margin-bottom: var(--unit);
  font-weight: 600;
  line-height: 1.3;
}

.email-display {
  color: var(--tertiary-text);
  font-size: 14px;
  line-height: 1.4;

  strong {
    color: var(--primary-text);
    font-weight: 600;
  }
}

.code-input-section {
  width: 100%;
  max-width: 320px;
  margin: var(--unit) 0;
}

.resend-section {
  margin-top: var(--unit);
}

.resend-link {
  background: none;
  border: none;
  color: var(--primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.2s ease;

  &:hover:not(:disabled) {
    color: var(--primary-dark);
    text-decoration: underline;
  }

  &:disabled {
    color: var(--tertiary-text);
    cursor: not-allowed;
  }
}

.button-set {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding-top: var(--wrapper);
  margin-top: auto;
}

.error-banner {
  background: var(--error-background, rgba(239, 68, 68, 0.1));
  color: var(--error, #ef4444);
  padding: 12px 16px;
  border-radius: var(--round-lg);
  text-align: center;
  font-size: 14px;
  margin-top: var(--unit);
  border: 1px solid var(--error-border, rgba(239, 68, 68, 0.2));
}
</style>