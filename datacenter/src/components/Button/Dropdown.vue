<template>
  <Menu as="div" class="dropdown-container relative inline-block text-left">
    <div>
      <MenuButton class="menu-button flex flex-col">
        <div class="header">
          <span class="_subtitle _color-secondary">{{ title }}</span>
          <ChevronDownIcon class="ChevronDownIcon _color-primary" />
        </div>
        <div class="input-box">
          {{ selectedFile || placeholder }}
        </div>
      </MenuButton>
    </div>

    <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
      <MenuItems class="menu-items flex flex-col absolute right-0 origin-top-right" :style="{ zIndex: 2 }">

        <!-- The container of items -->
        <div class="py-1 flex-col w-full">
          <MenuItem v-for="file in files" :key="file" v-slot="{ active }">
          <button @click="selectFile(file)" :class="[
            'block w-full text-left px-4 py-2 text-sm',
            active ?
              '._color-primary' : 'text-gray-700',
            file === selectedFile ? 'font-semibold' : ''
          ]"> {{ file }}
          </button>
          </MenuItem>
        </div>

      </MenuItems>
    </transition>

  </Menu>
</template>

<script setup>
import { ref, watch } from 'vue';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'

const emit = defineEmits(['selected']);

const props = defineProps({
  files: Array,
  modelValue: String,
  placeholder: {
    type: String,
    default: 'Select an option',
  },
  title: { type: String, default: '' }
});

const selectedFile = ref(props.modelValue || 'Select a file');

watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    selectedFile.value = newValue;
  }
});

function selectFile(file) {
  selectedFile.value = file;
  emit('selected', file);
}
</script>

<style lang="scss" scoped>
.header {
  justify-content: space-between;
  align-self: stretch;
  align-items: center;
  padding-left: 4px;
}

.menu-button {
  width: 200px;
  gap: 4px;
  align-items: center;
  justify-content: space-between;
  align-self: stretch;
  border-radius: var(--Border-Button-Round, 8px);
  background: #FFF;

  // 🏗️ TODO: Use the var of style.css
  color: rgba(0, 0, 0, 0.95);
  font-size: 15px;
  font-weight: 700;
  line-height: 24px;
}

.menu-items {
  width: 100%;
  margin-top: 4px;
  justify-content: center;
  align-items: flex-start;
  align-self: stretch;
  border-radius: var(--Border-Button-Round, 8px);
  background: #E9E9E9;
}

.input-box {
  width: 100%;
  height: 46px;
  padding: 12px;
  border-radius: 6px;
  background-color: #EDEDED;
  color: #7A7A7A;
  font-size: 18px;
  font-weight: 500;
  line-height: 26px;
}

.ChevronDownIcon {
  width: 24px;
  height: 24px;
}

.dropdown-container {
  width: auto;
}
</style>
