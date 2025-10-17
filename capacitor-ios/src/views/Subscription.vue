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

    <button @click="handlePurchase">Test Data</button>
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
  isPremium,
  loadOffering,
  purchaseSelected,
} = usePurchases()

const purchasing = ref(false)
const selectedPlan = ref('yearly')

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
  if (purchasing.value) return 'Processing...'
  if (isPremium.value) return 'Already Subscribed'
  return 'Start Free Trial for 7 days'
})

// WHY?
const handlePurchase = async () => {
  console.log('=== Purchase Debug ===')
  console.log('isPremium:', isPremium.value)
  if (!selectedPkg.value) {
    console.error('❌ No package selected!')
    return
  }

  try {
    purchasing.value = true
    console.log('💳 Starting purchase...')

    const success = await purchaseSelected()
    console.log('RevenueCat isPremium:', isPremium.value)

    if (success) {
      console.log('✅ Purchase successful!')
      console.log('📊 Before sync - isPremium:', userStore.isPremium)

      const synced = await userStore.syncPremiumStatus(
        selectedPkg.value.product.identifier,
        'active'
      )

      if (synced) {
        console.log('✅ Premium synced to backend!')
        console.log('📊 After sync - isPremium:', userStore.isPremium)
      }

      router.push('/account')
    }
  } catch (err) {
    console.error('❌ Purchase error:', err)
  } finally {
    purchasing.value = false
  }
}

onMounted(async () => {
  console.log('🔄 Loading offerings...')
  await loadOffering()
  console.log('✅ Offerings loaded!')
  console.log('📦 Packages:', packages.value.length)
  console.log('isPremium', userStore.isPremium)
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