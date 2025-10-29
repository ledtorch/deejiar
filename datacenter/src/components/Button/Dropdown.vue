<template>
  <Menu as="div" class="dropdown-container">
    <MenuButton class="menu-button">
      <div class="header">
        <span class="_subtitle _color-secondary">{{ title }}</span>
        <ChevronDownIcon class="ChevronDownIcon _color-primary" />
      </div>
      <p class="input-box _color-tertiary _body2 ">
        {{ selectedLabel || placeholder }}
      </p>
    </MenuButton>

    <MenuItems class="dropdown-menu">
      <MenuItem v-for="option in options" :key="option" v-slot="{ active }">
      <button @click="selectOption(option)" :class="['menu-item-button _color-tertiary',
        option === selectedLabel ? 'font-semibold' : ''
      ]"> {{ option }}
      </button>
      </MenuItem>
    </MenuItems>

  </Menu>
</template>

<script setup>
import { ref, watch } from 'vue';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'

const emit = defineEmits(['selected']);

const props = defineProps({
  options: Array,
  modelValue: String,
  placeholder: {
    type: String,
    default: 'Select an option',
  },
  title: { type: String, default: '' }
});

const selectedLabel = ref(props.modelValue || '?');

watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    selectedLabel.value = newValue;
  }
});

function selectOption(option) {
  selectedLabel.value = option;
  emit('selected', option);
}
</script>

<style lang="scss" scoped>
.dropdown-container {
  width: 100%;
  position: relative;
  display: inline-block;
  text-align: left;
}

.header {
  justify-content: space-between;
  align-self: stretch;
  align-items: center;
  padding-left: 4px;
}

.menu-button {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 4px;
  justify-content: space-between;
  border-radius: var(--Border-Button-Round, 8px);
  background: #FFF;

  color: var(--primary-text);
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

.input-box {
  text-align: left;
  width: 100%;
  height: 46px;
  padding: 12px;
  border-radius: 6px;
  background-color: #EDEDED;
  color: #7A7A7A;
}

.ChevronDownIcon {
  width: 24px;
  height: 24px;
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
