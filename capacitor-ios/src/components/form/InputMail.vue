<template>
  <input ref="inputRef" :class="['form-input', { 'form-input--on': editing }]" v-model="editingValue"
    :readonly="!editing" :placeholder="editing ? placeholder : ''" type=" email" @click="startEditing"
    @blur="handleBlur" @keyup.enter="handleSubmit" @keyup.escape="cancelEditing" />
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';

// Props
const props = defineProps({
  value: { type: String, default: '' },
  placeholder: { type: String, default: 'Unlock advance features with mail' },
  autoFocus: { type: Boolean, default: false }
});

// Emits
const emit = defineEmits(['update', 'editing-start', 'editing-end', 'submit']);

// Refs
const inputRef = ref(null);
const editing = ref(false);
const editingValue = ref(props.value || '');
const originalValue = ref(props.value || '');

// Keep input in sync when parent value changes (only when not editing)
watch(
  () => props.value,
  (val) => {
    if (!editing.value) {
      editingValue.value = val || '';
      originalValue.value = val || '';
    }
  }
);

// Auto focus when prop changes
watch(
  () => props.autoFocus,
  async (shouldFocus) => {
    if (shouldFocus && !editing.value) {
      await startEditing();
    }
  }
);

// Methods
const startEditing = async () => {
  if (!editing.value) {
    editing.value = true;
    originalValue.value = editingValue.value;

    // Focus the input after DOM update
    await nextTick();
    inputRef.value?.focus();

    emit('editing-start');
  }
};

const handleBlur = () => {
  // Don't auto-save on blur, let parent control when to save
  if (editing.value) {
    emit('editing-end', editingValue.value);
  }
};

const handleSubmit = () => {
  if (editing.value) {
    emit('submit', editingValue.value);
  }
};

const cancelEditing = () => {
  editingValue.value = originalValue.value;
  editing.value = false;
  inputRef.value?.blur();
  emit('editing-end', originalValue.value);
};

const saveValue = () => {
  if (editing.value) {
    emit('update', editingValue.value);
    editing.value = false;
    emit('editing-end', editingValue.value);
  }
};

const getCurrentValue = () => {
  return editingValue.value;
};

const isEditing = () => {
  return editing.value;
};

const focusInput = async () => {
  await startEditing();
};

// Expose methods for parent component
defineExpose({
  startEditing,
  saveValue,
  cancelEditing,
  getCurrentValue,
  isEditing,
  focusInput
});
</script>

<style lang="scss" scoped>
.form-input {
  width: 100%;
  height: 44px;
  padding: 12px;
  border: 1px solid var(--tertiary-text);
  border-radius: var(--round-m);
  box-sizing: border-box;

  background: var(--invert-content);
  color: var(--tertiary-text);

  font-family: inherit;
  font-size: 16px;
  outline: none;
  transition: all 0.2s ease;

  cursor: pointer;

  &::placeholder {
    color: var(--tertiary-text);
    opacity: 0.7;
  }

  &:hover:not(.form-input--on) {
    border-color: var(--secondary-text);
  }

  &--on {
    border-color: var(--baseline-green, #3dc363);
    color: var(--primary-text);
    cursor: text;

    &:focus {
      border-color: var(--baseline-green, #3dc363);
      box-shadow: 0 0 0 2px rgba(61, 195, 99, 0.2);
    }
  }

  // iOS zoom prevention
  @media screen and (max-width: 768px) {
    font-size: 16px;
  }
}
</style>