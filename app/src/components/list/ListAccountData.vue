<template>
  <section class="list-container" :class="containerClass">
    <div class="header" v-if="listData.icon">
      <div class="title-container">
        <img :src="listData.icon" class="title-icon icon-themed" />
        <p class="_title data-title">{{ listData.title }}</p>
      </div>
      <p class="_button-secondary temp-button-text"></p>
    </div>

    <div class="content">
      <p class="_body2 connected-account">
        {{ listData.account || 'Connect to unlock advance features' }}
      </p>
      <p v-if="listData.connectedDate" class="_body2 connected-date">
        {{ listData.connectedDate }}
      </p>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue';
import { useUserStore } from '../../stores/userStore';

import emailIcon from '@/assets/icons/action/email.svg'
import xIcon from '@/assets/icons/social/x.svg'
import instagramIcon from '@/assets/icons/social/instagram.svg'

const props = defineProps({
  email: {
    type: Boolean,
    default: false
  },
  x: {
    type: Boolean,
    default: false
  },
  instagram: {
    type: Boolean,
    default: false
  }
});

const userStore = useUserStore();

// Data for different variants
const listData = computed(() => {
  if (props.email) {
    return {
      icon: emailIcon,
      title: 'Registered Mail',
      account: userStore.userEmail,
      actionText: 'Update',
      connectedDate: userStore.formattedRegistrationDate
    };
  }

  if (props.x) {
    return {
      icon: xIcon,
      title: 'X(Twitter)',
      account: userStore.xAccount,
      actionText: 'Manage',
      connected: !!userStore.xAccount,
      connectedDate: userStore.formattedXConnectedDate
    };
  }

  if (props.instagram) {
    return {
      icon: instagramIcon,
      title: 'Instagram',
      account: userStore.instagramAccount,
      actionText: 'Connect',
      connected: !!userStore.instagramAccount,
      connectedDate: userStore.formattedInstagramConnectedDate
    };
  }

  // Default fallback
  return {
    icon: null,
    title: 'Default Title',
    subtitle: 'Default subtitle',
    actionText: null
  };
});

// Dynamic classes
const containerClass = computed(() => ({
  'list-container--connected': listData.value.connected,
  'list-container--disconnected': !listData.value.connected && props.instagram
}));

const subtitleClass = computed(() => ({
  'subtitle--connected': listData.value.connected,
  'subtitle--normal': !listData.value.connected && !props.instagram,
  'subtitle--prompt': props.instagram && !listData.value.connected
}));
</script>

<style lang="scss" scoped>
.list-container {
  /* Positioning */
  position: relative;

  /* Layout */
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 72px;
  padding: var(--box) var(--block);
  gap: var(--unit);

  /* Visual & Colors */
  background-color: var(--content);
  border-radius: var(--round-m);
}

.header {
  width: 100%;
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}

.title-container {
  gap: var(--atom);
}

.title-icon {
  width: 24px;
  height: 24px;
}

.data-title {
  color: var(--secondary-text);
}

.content {
  justify-content: space-between;
}

// TEMP
.temp-button-text {
  color: var(--tertiary-text);
}

.connected-date {
  max-width: 165px;
  color: var(--color-green);
}

.connected-account {
  text-overflow: ellipsis;
  color: var(--primary-text);
}
</style>