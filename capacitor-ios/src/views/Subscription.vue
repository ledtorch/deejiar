<template>
  <main class="page">
    <section class="main-container">
      <HeaderPage :pagetitle="'Join the Deejiar Pioneers'"></HeaderPage>
      <img :src="bannerImage" alt="">
      <div class="promote-feature-container">
        <TheAvatar overrideState="active" class="avatar-in-subscription" />
        <img src="/icon/action/arrow-right.svg" class="arrow-right-in-subscription">
        <TheAvatar overrideState="premium" class="avatar-in-subscription" />
      </div>
      <SubscriptionRadioCard :monthlyPackage="monthlyPkg" :yearlyPackage="yearlyPkg" :selectedId="selectedId"
        @select="selectPackage" />
    </section>

    <PrimaryButton :action="purchaseButtonText" :disabled="!selectedPkg || purchasing" @click="handlePurchase"
      default />
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import { usePurchases } from '../composables/usePurchase'

import HeaderPage from '../components/nav/HeaderPage.vue'
import PrimaryButton from '../components/button/CTA/PrimaryButton.vue'
import bannerImage from '@/assets/images/lv1-banner.svg'
import TheAvatar from '../components/button/TheAvatar.vue'
import SubscriptionRadioCard from '../components/cards/SubscriptionRadioCard.vue'

const router = useRouter()
const userStore = useUserStore()
const {
  packages,
  selectedId,
  selectedPkg,
  isPremium,
  loadOffering,
  purchaseSelected,
} = usePurchases()

const purchasing = ref(false)
const selectedPlan = ref('yearly')

// Button Animation
const loadingDots = ref('');

// SubscriptionRadioCard: Map UI on iOS
const monthlyPkg = computed(() =>
  packages.value.find(p => p.identifier === '$rc_monthly')
)

const yearlyPkg = computed(() =>
  packages.value.find(p => p.identifier === '$rc_annual')
)

const selectPackage = (packageId) => {
  console.log('📦 Package selected:', packageId)
  selectedId.value = packageId
}

/* Button Text */
const purchaseButtonText = computed(() => {
  if (purchasing.value) return `Processing${loadingDots.value}`
  if (isPremium.value) return 'Already Subscribed'
  return 'Start Free Trial for 7 days'
})

const startLoadingAnimation = () => {
  console.log('Animation started');
  let dotCount = 0;
  const loadingInterval = setInterval(() => {
    dotCount = (dotCount + 1) % 4; // 0, 1, 2, 3, then repeat
    loadingDots.value = '.'.repeat(dotCount);

    // Stop animation when no longer submitting
    if (!purchasing.value) {
      clearInterval(loadingInterval);
      loadingDots.value = '';
    }
  }, 500); // Change dots every 500ms
};

// WHY?
const handlePurchase = async () => {
  console.log('=== Purchase Debug ===')
  console.log('isPremium:', isPremium.value)
  startLoadingAnimation();
  if (!selectedPkg.value) {
    console.error('❌ No package selected!')
    return
  }

  try {
    purchasing.value = true
    startLoadingAnimation()
    console.log('💳 Starting purchase...')

    const success = await purchaseSelected()
    console.log('RevenueCat isPremium:', isPremium.value)

    if (success) {
      // 🏗️ Didn't handle the case if Supabase missed to update immediately
      await userStore.fetchCurrentUser()
      router.back()
    }
  } catch (err) {
    console.error('❌ Purchase error:', err)
  } finally {
    purchasing.value = false
  }
}

onMounted(async () => {
  try {
    console.log('🔄 Loading offerings...')
    await loadOffering()
    console.log('✅ Offerings loaded!')
    console.log('📦 Packages:', packages.value.length)
    console.log('isPremium', userStore.isPremium)
  } catch (error) {
    console.error('❌ Failed to load offerings, redirecting to account:', error)
    router.push({ name: 'account' })
  }
})
</script>

<style lang="scss" scoped>
.page {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100vw;
  height: 100vh;
  padding: var(--safe-area-top) var(--wrapper) env(safe-area-inset-bottom) var(--wrapper);

  /* Visual */
  background-color: var(--background);
}

.main-container {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  height: 100%;
  align-items: center;
  gap: var(--division);
}

.promote-feature-container {
  align-items: center;
  gap: var(--block);
}

.avatar-in-subscription {
  width: 44px;
  height: 44px;
}

.arrow-right-in-subscription {
  width: 24px;
  height: 24px;
}
</style>