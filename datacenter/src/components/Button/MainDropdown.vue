<template>
  <Menu as="div" class="dropdown-container">
    <MenuButton class="menu-button flex flex-row">
      <p class="_button-secondary button-text">
        {{ selectedLabel || placeholder }}
      </p>
      <ChevronDownIcon class="ChevronDownIcon _color-primary" />
    </MenuButton>

    <MenuItems class="dropdown-menu">
      <MenuItem class="menu-item" v-for="item in normalized" :key="item.value">
      <button @click="selectFile(item.value)" class="menu-item-button _color-tertiary"
        :class="{ 'font-semibold': item.value === modelValue }">
        {{ item.label }}
        <img v-if="item.value === modelValue" src="/icon/confirm.svg">
      </button>
      </MenuItem>
    </MenuItems>
  </Menu>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'

const emit = defineEmits(['update:modelValue', 'selected']);

const props = defineProps({
  options: {
    type: Array,
    default: () => []
  },
  modelValue: {
    type: [String, Number, Object, null],
    default: null
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Select a file'
  }
});

// Normalize `options` to [{ label, value }]
const normalized = computed(() =>
  (props.options || []).map(item => {
    if (item && typeof item === 'object' && 'label' in item && 'value' in item) return item;
    const s = String(item ?? '');
    return { label: s, value: s };
  })
);

// Determine label to show from current modelValue
const selectedLabel = computed(() => {
  if (props.modelValue == null || props.modelValue === '') return '';
  const found = normalized.value.find(i => i.value === props.modelValue);
  // If value not found (e.g., options just changed), show raw value string
  return found ? found.label : String(props.modelValue);
});

function selectFile(val) {
  emit('update:modelValue', val);
  emit('selected', val);
}

// If the current value disappears from the list, clear it
watch(() => props.options, () => {
  const exists = normalized.value.some(i => i.value === props.modelValue);
  if (!exists) emit('update:modelValue', null);
});
</script>

<style lang="scss" scoped>
.dropdown-container {
  width: auto;
  position: relative;
  display: inline-block;
  text-align: left;
}

.menu-button {
  min-width: 200px;
  width: auto;
  height: auto;
  padding: 9px;
  align-items: center;
  justify-content: space-between;
  align-self: stretch;
  border-radius: var(--Border-Button-Round, 8px);
  background: rgba(0, 0, 0, 0.95);
  color: rgba(0, 0, 0, 0.95);
}

.dropdown-menu {
  // Positioning
  position: absolute;
  right: 0;
  z-index: 2;

  // Layout
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  align-self: stretch;

  width: 100%;
  margin-top: 10px;
  padding: 8px 10px;

  // Style
  border-radius: var(--Border-Button-Round, 8px);
  background: #E9E9E9;
}

.menu-item {
  width: 100%;
}

.button-text {
  color: rgba(255, 255, 255, 0.95);
}

.ChevronDownIcon {
  width: 24px;
  height: 24px;
  color: rgba(255, 255, 255, 0.95);
}

// Dropdown menu
.menu-item-button {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 11px 0px 11px 12px;
  text-align: left;
}

.menu-item-button:hover {
  background: rgba(0, 0, 0, 0.14);
  border-radius: 8px;
}

.menu-item-button:active {
  background: rgba(0, 0, 0, 0.3);
}
</style>
