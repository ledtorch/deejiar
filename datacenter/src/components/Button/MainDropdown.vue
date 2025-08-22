<template>
  <Menu as="div" class="relative inline-block text-left">
    <div>
      <MenuButton class="menu-button flex flex-row">
        <p class="_button-secondary button-text">
          {{ selectedLabel || placeholder }}
        </p>
        <ChevronDownIcon class="ChevronDownIcon _color-primary" />
      </MenuButton>
    </div>

    <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
      <MenuItems class="menu-items flex flex-col absolute right-0 origin-top-right" :style="{ zIndex: 2 }">
        <div class="py-1 flex-col w-full">
          <MenuItem class="menu-item" v-for="item in normalized" :key="item.value">
          <button @click="selectFile(item.value)" class="menu-item-button"
            :class="{ 'font-semibold': item.value === modelValue }">
            {{ item.label }}
          </button>
          </MenuItem>
        </div>
      </MenuItems>
    </transition>
  </Menu>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'

const emit = defineEmits(['update:modelValue', 'selected']);

const props = defineProps({
  files: {
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

// Normalize `files` to [{ label, value }]
const normalized = computed(() =>
  (props.files || []).map(item => {
    if (item && typeof item === 'object' && 'label' in item && 'value' in item) return item;
    const s = String(item ?? '');
    return { label: s, value: s };
  })
);

// Determine label to show from current modelValue
const selectedLabel = computed(() => {
  if (props.modelValue == null || props.modelValue === '') return '';
  const found = normalized.value.find(i => i.value === props.modelValue);
  // If value not found (e.g., files just changed), show raw value string
  return found ? found.label : String(props.modelValue);
});

function selectFile(val) {
  emit('update:modelValue', val);
  emit('selected', val);
}

// If the current value disappears from the list, clear it
watch(() => props.files, () => {
  const exists = normalized.value.some(i => i.value === props.modelValue);
  if (!exists) emit('update:modelValue', null);
});
</script>

<style lang="scss" scoped>
.header {
  justify-content: space-between;
  align-self: stretch;
  padding-left: 4px;
}

.menu-button {
  min-width: 200px;
  width: auto;
  height: 48px;
  padding: 12px;
  align-items: center;
  justify-content: space-between;
  align-self: stretch;
  border-radius: var(--Border-Button-Round, 8px);
  background: rgba(0, 0, 0, 0.95);

  // 🏗️ TODO: Use the var of style.css
  color: rgba(0, 0, 0, 0.95);
  font-size: 15px;
  font-weight: 700;
  line-height: 24px;
}

.menu-items {
  width: 100%;
  margin-top: 4px;
  padding: 8px 10px;
  justify-content: center;
  align-items: flex-start;
  align-self: stretch;
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

.menu-item-button {
  display: block;
  width: 100%;
  text-align: left;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  color: #4b5563; // default gray
}

.menu-item-button:hover {
  background: rgba(0, 0, 0, 0.14);
  border-radius: 8px;
}

.menu-item-button:active {
  background: rgba(0, 0, 0, 1);
}
</style>
