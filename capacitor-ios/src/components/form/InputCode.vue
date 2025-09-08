<template>
  <div class="code-box" :class="{ 'error': hasError, 'filled': codeValue.length > 0 }">
    <input ref="codeInput" v-model="codeValue" type="tel" inputmode="numeric" pattern="[0-9]*" maxlength="6"
      placeholder="Code" class="code-input" @input="handleCodeInput" @focus="handleFocus" @blur="handleBlur"
      @paste="handleCodePaste" @keydown="handleKeydown" />
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
  }
});

const emit = defineEmits(['update:modelValue', 'complete', 'editing-start', 'editing-end']);

// Refs
const codeInput = ref(null);
const codeValue = ref('');
const isEditing = ref(false);

// Computed
const isComplete = computed(() => {
  return codeValue.value.length === 6;
});

// Watch for external value changes
watch(() => props.modelValue, (newValue) => {
  if (newValue !== codeValue.value) {
    codeValue.value = newValue;
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
const handleCodeInput = (event) => {
  let value = event.target.value;

  // Only allow numbers
  value = value.replace(/\D/g, '');

  // Limit to 6 digits
  if (value.length > 6) {
    value = value.slice(0, 6);
  }

  codeValue.value = value;

  // Auto-complete when 6 digits entered
  if (value.length === 6) {
    emit('complete', value);
  }
};

const handleCodePaste = (event) => {
  event.preventDefault();
  const pastedData = event.clipboardData.getData('text');
  const digits = pastedData.replace(/\D/g, '').slice(0, 6);

  codeValue.value = digits;

  if (digits.length === 6) {
    emit('complete', digits);
  }
};

const handleKeydown = (event) => {
  // Handle Enter key
  if (event.key === 'Enter' && isComplete.value) {
    emit('complete', codeValue.value);
  }

  // Allow backspace, delete, tab, escape, enter
  if ([8, 9, 27, 13, 46].indexOf(event.keyCode) !== -1 ||
    // Allow Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
    (event.keyCode === 65 && event.ctrlKey === true) ||
    (event.keyCode === 67 && event.ctrlKey === true) ||
    (event.keyCode === 86 && event.ctrlKey === true) ||
    (event.keyCode === 88 && event.ctrlKey === true)) {
    return;
  }

  // Ensure that it is a number and stop the keypress
  if ((event.shiftKey || (event.keyCode < 48 || event.keyCode > 57)) && (event.keyCode < 96 || event.keyCode > 105)) {
    event.preventDefault();
  }
};

const handleFocus = () => {
  if (!isEditing.value) {
    isEditing.value = true;
    emit('editing-start');
  }
};

const handleBlur = () => {
  if (isEditing.value) {
    isEditing.value = false;
    emit('editing-end');
  }
};

const focus = () => {
  codeInput.value?.focus();
};

const clear = () => {
  codeValue.value = '';
  focus();
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
.code-box {
  background: var(--content);
  display: flex;
  height: 44px;
  padding: var(--unit) var(--block);
  justify-content: center;
  align-items: center;
  border-radius: var(--round-m);
  border: 0.5px solid var(--tertiary-text);

  transition: all 0.2s ease;

  &:focus-within {
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
}

.code-input {
  width: 100%;
  border: none;
  outline: none;
  background: transparent;
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  color: var(--primary-text);
  letter-spacing: 0.5em;

  // Remove default input styling
  -webkit-appearance: none;
  -moz-appearance: textfield;

  &::-webkit-outer-spin-button,
  &::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  &::placeholder {
    color: var(--tertiary-text);
    letter-spacing: normal;
  }

  &:disabled {
    color: var(--disabled-text);
    cursor: not-allowed;
  }
}
</style>