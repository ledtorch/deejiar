<template>
  <div class="code-input-wrapper">
    <div class="code-input-container">
      <input v-for="(digit, index) in codeDigits" :key="index" :ref="el => codeInputs[index] = el"
        v-model="codeDigits[index]" type="tel" inputmode="numeric" pattern="[0-9]*" maxlength="1" class="code-digit"
        :class="{ 'filled': codeDigits[index] !== '', 'error': hasError }" @input="handleCodeInput(index, $event)"
        @keydown="handleCodeKeydown(index, $event)" @paste="handleCodePaste($event)" @focus="handleFocus(index)"
        @blur="handleBlur" />
    </div>
    <div v-if="hasError" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  autoFocus: {
    type: Boolean,
    default: false
  },
  hasError: {
    type: Boolean,
    default: false
  },
  errorMessage: {
    type: String,
    default: 'Invalid code'
  }
});

const emit = defineEmits(['update:modelValue', 'complete', 'editing-start', 'editing-end']);

// Refs
const codeInputs = ref([]);
const codeDigits = ref(['', '', '', '', '', '']);
const isEditing = ref(false);

// Computed
const isComplete = computed(() => {
  return codeDigits.value.every(digit => digit !== '');
});

const codeValue = computed(() => {
  return codeDigits.value.join('');
});

// Watch for external value changes
watch(() => props.modelValue, (newValue) => {
  if (newValue !== codeValue.value) {
    const digits = newValue.padEnd(6, '').slice(0, 6).split('');
    codeDigits.value = digits;
  }
});

// Watch for internal changes
watch(codeValue, (newValue) => {
  emit('update:modelValue', newValue);

  if (isComplete.value) {
    emit('complete', newValue);
  }
});

// Methods
const handleCodeInput = (index, event) => {
  const value = event.target.value;

  // Only allow single digit
  if (value.length > 1) {
    codeDigits.value[index] = value.slice(-1);
    return;
  }

  // Only allow numbers
  if (!/^\d*$/.test(value)) {
    event.target.value = codeDigits.value[index];
    return;
  }

  codeDigits.value[index] = value;

  // Auto-focus next input
  if (value && index < 5) {
    codeInputs.value[index + 1]?.focus();
  }
};

const handleCodeKeydown = (index, event) => {
  // Handle backspace
  if (event.key === 'Backspace') {
    if (!codeDigits.value[index] && index > 0) {
      // Move to previous input if current is empty
      codeInputs.value[index - 1]?.focus();
    } else if (codeDigits.value[index]) {
      // Clear current input
      codeDigits.value[index] = '';
    }
  }

  // Handle arrow keys
  if (event.key === 'ArrowLeft' && index > 0) {
    codeInputs.value[index - 1]?.focus();
  }

  if (event.key === 'ArrowRight' && index < 5) {
    codeInputs.value[index + 1]?.focus();
  }

  // Handle Enter key
  if (event.key === 'Enter' && isComplete.value) {
    emit('complete', codeValue.value);
  }
};

const handleCodePaste = (event) => {
  event.preventDefault();
  const pastedData = event.clipboardData.getData('text');
  const digits = pastedData.replace(/\D/g, '').slice(0, 6).split('');

  // Fill digits
  digits.forEach((digit, index) => {
    if (index < 6) {
      codeDigits.value[index] = digit;
    }
  });

  // Focus appropriate input
  const lastFilledIndex = Math.min(digits.length - 1, 5);
  const nextEmptyIndex = codeDigits.value.findIndex(digit => digit === '');

  if (nextEmptyIndex !== -1) {
    codeInputs.value[nextEmptyIndex]?.focus();
  } else {
    codeInputs.value[lastFilledIndex]?.focus();
  }
};

const handleFocus = (index) => {
  if (!isEditing.value) {
    isEditing.value = true;
    emit('editing-start');
  }
};

const handleBlur = () => {
  // Check if focus moved to another code input
  setTimeout(() => {
    const activeElement = document.activeElement;
    const isCodeInputFocused = codeInputs.value.some(input => input === activeElement);

    if (!isCodeInputFocused && isEditing.value) {
      isEditing.value = false;
      emit('editing-end');
    }
  }, 0);
};

const focus = () => {
  const firstEmptyIndex = codeDigits.value.findIndex(digit => digit === '');
  const indexToFocus = firstEmptyIndex !== -1 ? firstEmptyIndex : 0;
  codeInputs.value[indexToFocus]?.focus();
};

const clear = () => {
  codeDigits.value = ['', '', '', '', '', ''];
  codeInputs.value[0]?.focus();
};

const getCurrentValue = () => {
  return codeValue.value;
};

// Auto-focus on mount
onMounted(() => {
  if (props.autoFocus) {
    nextTick(() => {
      focus();
    });
  }
});

// Expose methods
defineExpose({
  focus,
  clear,
  getCurrentValue
});
</script>

<style lang="scss" scoped>
.code-input-wrapper {
  width: 100%;
}

.code-input-container {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 8px;
}

.code-digit {
  width: 48px;
  height: 56px;
  border: 2px solid var(--border-light);
  border-radius: var(--round-lg);
  text-align: center;
  font-size: 24px;
  font-weight: 600;
  background: var(--input-background, #ffffff);
  color: var(--primary-text);
  transition: all 0.2s ease;

  // Remove default input styling
  -webkit-appearance: none;
  -moz-appearance: textfield;

  &::-webkit-outer-spin-button,
  &::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  &:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.1);
  }

  &.filled {
    border-color: var(--success, var(--primary));
    background: var(--success-background, rgba(var(--primary-rgb), 0.05));
  }

  &.error {
    border-color: var(--error);
    background: var(--error-background, rgba(var(--error-rgb), 0.05));
  }

  &:disabled {
    background: var(--disabled-background);
    color: var(--disabled-text);
    cursor: not-allowed;
  }
}

.error-message {
  color: var(--error);
  font-size: 12px;
  text-align: center;
  margin-top: 4px;
  min-height: 16px;
}
</style>