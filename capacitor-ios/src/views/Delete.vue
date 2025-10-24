<template>
  <main class="page">
    <section class="main-container">
      <div class="upper-container">
        <HeaderPage :pagetitle="'Delete Account'" />

        <img :src="PageIllustration" class="page-illustration">
        <p class="_body1">
          <strong>Sorry to see you go =(</strong>
        </p>

        <p class="_body1">
          Your account will be scheduled for deletion and fully removed after 30 days.
        </p>

        <p class="_body1">
          If you have an active subscription, you will keep your premium benefits until they expire.
        </p>

        <p class="_body1">
          You may request account recovery before <strong>{{ deletionDeadline }}</strong>, by emailing
          <strong>hi@deejiar.com</strong>.
        </p>

        <p class="_body1">
          Please consider this action carefully. It can <strong>NOT</strong> be undone after the deadline.
        </p>

        <Divider />
      </div>

      <PrimaryButton action="Delete Account" class="temp-danger-button" default @click="deleteAccount" />
    </section>
  </main>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/userStore';
import HeaderPage from '../components/nav/HeaderPage.vue';
import Divider from '../components/common/Divider.vue';
import PrimaryButton from '../components/button/CTA/PrimaryButton.vue';
import PageIllustration from '@/assets/illustration/illu-delete-account.jpg';

const router = useRouter();
const API_ENDPOINT = import.meta.env.VITE_API_URL;
const userStore = useUserStore();

// Computed deletion deadline: Today + 30 days at 23:59
const deletionDeadline = computed(() => {
  const today = new Date();
  const deadline = new Date(today);
  deadline.setDate(today.getDate() + 30);

  // Format: "Nov 20, 23:59"
  const monthNames = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
  ];

  const month = monthNames[deadline.getMonth()];
  const day = deadline.getDate();

  return `${month} ${day}, 23:59`;
});

const deleteAccount = async () => {
  // Show confirmation dialog
  const confirmed = confirm(
    `Are you absolutely sure?\n\n` +
    `Your account will be deleted on ${deletionDeadline.value}.\n\n` +
    `This action cannot be undone after the deadline.`
  );

  if (!confirmed) {
    return;
  }

  try {
    const token = userStore.accessToken;

    if (!token) {
      alert('You must be logged in to delete your account');
      router.push('/login');
      return;
    }

    console.log('[deleteAccount] Scheduling account deletion...');

    // Call the delete account API endpoint
    const response = await fetch(`${API_ENDPOINT}/user/auth/delete`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }
    });

    if (response.ok) {
      const result = await response.json();
      console.log('[deleteAccount] ✅ Account deletion scheduled:', result);

      alert(
        `Account deletion scheduled.\n\n` +
        `You have until ${deletionDeadline.value} to recover your account by emailing hi@deejiar.com`
      );

      // Log out and redirect
      await userStore.logout();
      router.push('/');
    } else {
      const error = await response.json();
      console.error('[deleteAccount] ❌ Failed:', error);
      alert(`Failed to delete account: ${error.detail || 'Unknown error'}`);
    }

  } catch (error) {
    console.error('[deleteAccount] Error:', error);
    alert('An error occurred while deleting your account. Please try again.');
  }
};
</script>

<style lang="scss" scoped>
.page {
  /* Positioning */
  position: relative;

  /* Layout */
  display: flex;
  flex-direction: column;
  min-width: 100%;
  justify-content: space-between;
  width: 100vw;
  height: 100vh;
  padding: var(--safe-area-top) var(--wrapper) env(safe-area-inset-bottom) var(--wrapper);

  /* Visual & Colors */
  background-color: var(--background);
}

.main-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--division);
}

.main-container> :first-child {
  flex: 1;
}

.main-container> :last-child {
  flex: 0 0 auto;
}

.upper-container {
  flex-direction: column;
  width: 100%;
  gap: var(--division);
}

.page-illustration {
  border-radius: var(--round-l);
}

.temp-danger-button {
  color: var(--primary-text);
  background-color: var(--color-red);
}
</style>