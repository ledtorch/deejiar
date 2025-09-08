<template>
  <section class="auth-container" ref="panelContainer">
    <div class="otp-content">

      <img src="/illustration/inbox.png" class="inbox-icon">
      <h4 class="auth-otp-heading">Check your mailbox to finish signing in</h4>

      <!-- 6-Digit Code Input -->
      <div class="code-input-section">
        <span class="_footnote email-display">We sent your code to</span>
        <span class="_footnote user-email">{{ userEmail }}</span>
        <InputCode ref="codeInputRef" v-model="otpCode" :autoFocus="true" :hasError="hasCodeError"
          :errorMessage="codeErrorMessage" @complete="handleCodeComplete" @editing-start="handleCodeEditingStart" />
      </div>

      <!-- Resend Helper -->
      <button class="resend-link _button-secondary" @click="resendCode" :disabled="!canResend"
        :style="{ color: resendColor }">
        {{ resendText }}
      </button>
    </div>

    <div class="button-set">
      <NeutralButton action="Back" type="icon-left" icon="arrow-left" @click="handleBack" />
      <PrimaryButton action="Verify" type="icon-right" icon="arrow-right" @click="submitCode" :loading="isVerifying"
        :disabled="!isCodeComplete" />
    </div>

  </section>
</template>

<script setup>
import { ref, computed, nextTick, inject, onMounted, onUnmounted } from 'vue';

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
    default: 'register'
  }
});

const emit = defineEmits(['close', 'auth-success']);

// Refs
const panelContainer = ref(null);
const codeInputRef = ref(null);
const bottomSheetControls = inject('bottomSheetControls');

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

// Event handlers
const handleCodeEditingStart = () => {
  clearErrors();
};

const handleCodeComplete = (code) => {
  if (code.length === 6) {
    // Auto-submit when code is complete
    submitCode();
  }
};

const handleBack = () => {
  bottomSheetControls.switchPanel('auth');
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
      bottomSheetControls.switchPanel('search');
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

// Resend code handlers
const canResend = computed(() => !resendCooldown.value && !isResending.value);

const resendText = computed(() =>
  resendCooldown.value ? `Resend in ${resendCooldown.value}s` :
    isResending.value ? 'Sending...' :
      "Didn't receive a code?"
);

const resendColor = computed(() =>
  resendCooldown.value ? 'var(--tertiary-text)' :
    isResending.value ? 'var(--color-green)' :
      'var(--color-yellow)'
);

// Lifecycle
onMounted(() => {
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
  align-items: center;
  gap: var(--section);
  padding: var(--section) var(--wrapper) var(--section) var(--wrapper);
}

.otp-content {
  flex-direction: column;
  align-items: center;
  gap: var(--division);
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
  color: var(--tertiary-text);
  text-align: center;
}

.code-input-section {
  flex-direction: column;
  width: 240px;
  align-items: center;
  background: var(--invert-content);
  border-radius: var(--round-l);
  gap: var(--box);
  padding: var(--block) var(--wrapper);
}

.resend-link {
  cursor: pointer;
  transition: color 0.2s ease;
}

.email-display {
  color: var(--tertiary-text);
}

.user-email {
  font-weight: 600;
  color: var(--secondary-text);
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
  border-radius: var(--round-l);
  text-align: center;
  font-size: 14px;
  margin-top: var(--unit);
  border: 1px solid var(--error-border, rgba(239, 68, 68, 0.2));
}
</style>