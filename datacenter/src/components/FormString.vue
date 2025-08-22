<template>
  <div class="form-frame">
    <div class="nav">
      <p class="_subtitle the-title">{{ title }}</p>
      <!-- Only show the Edit button when editing is false -->
      <button class="text-button" v-if="!editing" @click="edit(property)">Edit</button>
      <!-- Only show the Save button when editing is true -->
      <button class="text-button" v-if="editing" @click="save">Save</button>
    </div>
    <input :class="['input-base', { input: !editing, 'input-on': editing }]" v-model="editingValue"
      :readonly="!editing" />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const emit = defineEmits(['update']);

const props = defineProps({
  value: { type: [Object, String, Number, Boolean, Array, null], default: null },
  property: { type: String, required: true },
  // used in original save() but not declared; keep for compatibility
  variant: { type: String, default: '' },
  title: { type: String, default: '' }
});

const editing = ref(false);
const editingValue = ref(props.value);

// keep input in sync when parent value changes (only when not editing)
watch(
  () => props.value,
  (val) => {
    if (!editing.value) editingValue.value = val;
  },
  { deep: true }
);

function edit(prop) {
  // 🐞 Debug console (kept from original)
  console.log('Value[property]: ' + (props.value && typeof props.value === 'object' ? props.value[prop] : props.value));

  editing.value = true;
  const val = (props.value && typeof props.value === 'object' && prop in props.value)
    ? props.value[prop]
    : props.value;
  editingValue.value = (val ?? '').toString();
}

function save() {
  const valueToEmit = props.variant === 'number' ? parseFloat(editingValue.value) : editingValue.value;
  emit('update', [props.property, valueToEmit]);
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

// Temp

.temp-button {
  cursor: pointer;
  background-color: transparent;
  border: 0px;
  padding: 10px 16px;
  justify-content: center;
  align-items: center;
  border-radius: var(--border-button-round, 8px);
  background: var(--token-theme, #fafafa);
  color: var(--token-invert, #0e0d0f);

  font-family: Be Vietnam Pro;
  font-size: 15px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;
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
