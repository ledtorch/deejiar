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
      <SubscriptionRadioCard :packages="packages" :selectedPlan="selectedPlan" @planSelected="handlePlanSelected" />
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
  loading,
  error,
  packages,
  selectedId,
  selectedPkg,
  premiumActive,
  loadOffering,
  purchaseSelected,
} = usePurchases()

const purchasing = ref(false)
const selectedPlan = ref('yearly')

const purchaseButtonText = computed(() => {
  if (purchasing.value) return 'Processing...'
  if (premiumActive.value) return 'Already Subscribed'
  return 'Start Free Trial for 7 days'
})

const handlePlanSelected = (plan) => {
  selectedPlan.value = plan

  // ✅ Map UI selection to RevenueCat package identifier
  selectedId.value = plan === 'monthly' ? '$rc_monthly' : '$rc_annual'
}

const handlePurchase = async () => {
  if (!selectedPkg.value) return

  try {
    purchasing.value = true
    const success = await purchaseSelected()

    if (success) {
      userStore.updateUserProfile({
        premium: true,
        subscription_plan: selectedPkg.value.product.identifier,
        subscription_status: 'active'
      })

      router.push('/profile')
    }
  } catch (err) {
    console.error('[Subscription] Purchase error:', err)
  } finally {
    purchasing.value = false
  }
}

onMounted(async () => {
  await loadOffering()
})
</script>

<style lang="scss" scoped>
.page {
  /* Positioning */
  position: relative;

  /* Layout & Box Model */
  display: flex;
  flex-direction: column;
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