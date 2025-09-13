<template>
  <section class="search-container">
    <div class="search-component">
      <TheSearch />
      <Close @close="closeBottomSheet" />
    </div>
  </section>
</template>

<script setup>
import TheSearch from '../../TheSearch.vue';
import Close from '../../button/Icon/Close.vue';
import PrimaryButton from '../../button/CTA/PrimaryButton.vue';
import { inject, computed } from 'vue';
import { useUserStore } from '../../../stores/userStore';
import { useRouter } from 'vue-router';


const router = useRouter();
const userStore = useUserStore();

const emit = defineEmits(['close', 'height-change']);
const bottomSheetControls = inject('bottomSheetControls', null);

const closeBottomSheet = () => {
  emit("close");
};
</script>

<style lang="scss" scoped>
.search-container {
  display: flex;
  flex-direction: column;
  padding: 0 var(--wrapper);
}

.search-component {
  justify-content: space-between;
  gap: var(--block);
}

.avatar-layout {
  width: 36px;
  height: 36px;
}

.collection-container {
  flex-direction: column;
  gap: var(--box);
  padding: var(--block) 0 var(--wrapper) 0;
}

.collection-title {
  color: var(--tertiary-text);
}
</style>