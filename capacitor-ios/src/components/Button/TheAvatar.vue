<template>
  <div class="avatar-container" :class="avatarContainerClass" @click="clickAvatar">
    <!-- Default: Icon only -->
    <div v-if="userState === 'default'" class="default-icon"></div>

    <!-- Active: Image only -->
    <img v-if="userState === 'active'" :src="profileImage" :alt="userName" class="avatar-image avatar-image--active" />

    <!-- Premium: + Ring & Medal -->
    <template v-if="userState === 'premium'">
      <div class="avatar-ring"></div>
      <img :src="profileImage" :alt="userName" class="avatar-image avatar-image--premium" />
      <div class="premium-medal"></div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  userState: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'active', 'premium'].includes(value)
  },
  profileImage: {
    type: String,
    default: '/images/example-avatar.jpg'
  },
  userName: {
    type: String,
    default: 'User'
  }
});

const router = useRouter();

// Computed classes for consistent scaling
const avatarContainerClass = computed(() => ({
  'avatar-container--default': props.userState === 'default',
  'avatar-container--logged-in': props.userState !== 'default'
}));

const clickAvatar = () => {
  if (props.userState === 'default') {
    router.push({ name: "subscription" });
  } else {
    router.push({ name: "account" });
  }
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

  /* Layout & Box Model */
  width: 46px;
  height: 46px;
  border-radius: 50%;
  border: 2px solid var(--color-green);
}

.avatar-image {
  /* Layout & Box Model */
  border-radius: 50%;

  /* Visual & Colors */
  object-fit: cover;

  &--active {
    /* Active: Full container size (44x44) */
    width: 100%;
    height: 100%;
  }

  &--premium {
    /* Premium: Centered inside ring */
    position: relative;
    z-index: 2;
    width: 40px;
    height: 40px;
  }
}

.premium-medal {
  /* Positioning */
  position: absolute;
  bottom: 0;
  right: 0;
  z-index: 3;

  /* Layout & Box Model */
  width: 16px;
  height: 16px;

  /* Visual & Colors */
  background-image: url('/icon/subscription-medal/trailblazer.png');
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