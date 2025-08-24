<template>
  <div class="form-frame">
    <div class="nav">
      <p class="_subtitle the-title">{{ title }}</p>
      <button class="text-button" v-if="!editing" @click="edit">Edit</button>
      <button class="text-button" v-if="editing" @click="save">Save</button>
    </div>
    <input :class="['input-base', { input: !editing, 'input-on': editing }]" v-model="editingValue"
      :readonly="!editing" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const emit = defineEmits(['update']);

const props = defineProps({
  title: { type: String, default: '' },
  value: { type: [String, Number], default: '' },
  placeholder: { type: String, default: '' },
  variant: { type: String, default: '' }
});

const editing = ref(false);
const editingValue = ref(String(props.value ?? ''));

// keep input in sync when parent value changes (only when not editing)
watch(
  () => props.value,
  (val) => {
    if (!editing.value) editingValue.value = String(val ?? '');
  }
);

function edit() {
  editing.value = true;
}

function save() {
  const out = props.variant === 'number' ? Number(editingValue.value) : editingValue.value;
  emit('update', out);
  editing.value = false;
}
</script>

<style lang="scss" scoped>
.input {
  height: 46px;
  width: auto;
  padding: 12px;
  justify-content: space-between;
  align-items: center;
  border-radius: var(--border-content, 6px);
  background: var(--base);
  color: var(--tertiary-text);
}

.nav {
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}

.form-frame {
  width: 100%;
  min-width: 200px;
  flex-grow: 1;
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  gap: 4px;
}

.headline {
  font-size: 16px;
  font-weight: 500;
  line-height: 21px;
  color: var(--3-text-dark-2nd-white,
      var(--token-secondary-text, rgba(255, 255, 255, 0.75)));
}

.input,
.input-on {
  width: auto;
  padding: 12px;
  border: 1px solid transparent;
  /* Ensures border width is included in height calculations */
  border-radius: var(--border-content, 6px);
  box-sizing: border-box;
  /* Includes padding and border in the element's total width and height */
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
  height: 50px;
  /* Explicitly setting the height */
}

.input-on {
  border: 1px solid var(--baseline-green, #3dc363);
  color: var(--primary-text);
  background: var(--base);
}

.text-button {
  cursor: pointer;
  color: var(--2-brand-gray, #808cab);
  background-color: transparent;
  padding: 0px;

  font-family: Be Vietnam Pro;
  font-size: 15px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;
}

.the-title {
  padding: 0px 4px;
  color: var(--secondary-text);
}

.input-base {
  height: 46px;
}
</style>
