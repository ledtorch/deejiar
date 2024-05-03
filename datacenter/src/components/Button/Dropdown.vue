<template>
  <Menu as="div" class="relative inline-block text-left">

    <div>
      <MenuButton class="menu-button flex">
        {{ selectedFile || 'Select a file' }}
        <ChevronDownIcon class="-mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
      </MenuButton>
    </div>

    <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
      <MenuItems class="menu-items flex flex-col absolute right-0 origin-top-right">

        <!-- The container of items -->
        <div class="py-1 flex flex-col w-full">
          <MenuItem v-for="file in files" :key="file" @click="selectFile(file)">
          <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">{{ file }}</a>
          </MenuItem>
        </div>

      </MenuItems>
    </transition>

  </Menu>
</template>

<script setup>
import { ref } from 'vue';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'

const emit = defineEmits(['selected']);

const props = defineProps({
  files: Array
});

const selectedFile = ref('');

function selectFile(file) {
  selectedFile.value = file;
  emit('selected', file);
}
</script>

<style lang="scss" scoped>
.menu-button {
  padding: 10px 12px;
  align-items: center;
  justify-content: space-between;
  align-self: stretch;
  border-radius: var(--Border-Button-Round, 8px);
  background: #FFF;
}

.menu-items {
  justify-content: center;
  align-items: flex-start;
  align-self: stretch;
  border-radius: var(--Border-Button-Round, 8px);
  background: var(--Base-Solid-base, #F2F2F2);
}
</style>
