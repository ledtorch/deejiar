<template>
  <div class="avatar-container" :class="avatarContainerClass" @click="clickAvatar">
    <!-- Default: Icon only -->
    <div v-if="currentUserState === 'default'" class="default-icon"></div>

    <!-- Active: Image only -->
    <img v-if="currentUserState === 'active'" :src="'/images/default-avatar.jpg'" :alt="displayName"
      class="avatar-image" @error="handleImageError" />

    <!-- Premium: + Ring & Medal -->
    <template v-if="currentUserState === 'premium'">
      <div class="avatar-ring"></div>
      <img :src="'/images/default-avatar.jpg'" class="avatar-image avatar-image--premium" @error="handleImageError" />
      <div class="premium-medal"></div>
    </template>
  </div>
</template>

<script setup>
import { computed, inject, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../../stores/userStore';

const props = defineProps({
  // Allow override for preview/demo purposes
  overrideState: {
    type: String,
    default: null,
    validator: (value) => !value || ['default', 'active', 'premium'].includes(value)
  },
  useBottomSheet: {
    type: Boolean,
    default: false
  }
});

const router = useRouter();
const userStore = useUserStore();
const bottomSheetControls = inject('bottomSheetControls', null);

// Use a fallback image if user has no avatar
const fallbackAvatar = '/images/default-avatar.png';
const imageLoadError = ref(false);

// Computed properties from user store
const currentUserState = computed(() => {
  // Allow override for demo/preview
  if (props.overrideState) return props.overrideState;

  // Use actual user state from store
  return userStore.userState;
});

// Computed classes for consistent scaling
const avatarContainerClass = computed(() => ({
  'avatar-container--default': currentUserState.value === 'default',
  'avatar-container--logged-in': currentUserState.value !== 'default'
}));

const handleImageError = () => {
  imageLoadError.value = true;
};

const clickAvatar = () => {
  if (currentUserState.value === 'default') {
    // User is not logged in - show authentication
    if (props.useBottomSheet && bottomSheetControls) {
      bottomSheetControls.switchPanel('auth');
    }
    return;  // Exit early
  }

  // User is logged in - navigate to account page
  router.push({ name: 'account' });
};
</script>

<style lang="scss" scoped>
.avatar-container {
  /* Positioning */
  position: relative;

  /* Layout & Box Model */
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;

  /* Interactions */
  cursor: pointer;

  /* Animations & Transitions */
  transition: all 0.2s ease;

  &:hover {
    transform: scale(1.05);
  }

  &:active {
    transform: scale(0.95);
  }

  // Default state: Simple background for icon
  &--default {
    border-radius: 50%;
    background: var(--primary-text);
  }
}

.default-icon {
  /* Layout & Box Model */
  width: 24px;
  height: 24px;

  /* Visual & Colors */
  background-image: url('/icon/action/account.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  filter: brightness(0) saturate(100%) invert(2%) sepia(8%) saturate(2618%) hue-rotate(309deg) brightness(97%) contrast(85%);
}

.avatar-ring {
  /* Positioning */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;

  /* Layout & Box Model */
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid var(--color-green);
}

.avatar-image {
  /* Layout & Box Model */
  border-radius: 50%;

  /* Visual & Colors */
  object-fit: cover;

  width: 100%;
  height: 100%;

  &--premium {
    /* Premium: Centered inside ring */
    position: relative;
    z-index: 1;
  }
}

.premium-medal {
  /* Positioning */
  position: absolute;
  bottom: 0;
  right: 0;
  z-index: 3;

  /* Layout & Box Model */
  width: 37.5%;
  height: 37.5%;

  /* Visual & Colors */
  background-image: url('@/assets/icons/subscription-medal/trailblazer.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

/* Fallback scaling using parent container size */
.avatar-container[data-size="large"] {
  .avatar-ring {
    width: 46px;
    height: 46px;
  }

  .avatar-image {
    width: 44px;
    height: 44px;
  }

  .premium-medal {
    width: 20px;
    height: 20px;
    bottom: -3px;
    right: -3px;
  }
}
</style>