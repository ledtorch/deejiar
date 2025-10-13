// src/composables/usePurchases.js
import { ref, computed } from 'vue'
import { Capacitor } from '@capacitor/core'
import { Purchases } from '@revenuecat/purchases-capacitor'

export function usePurchases() {
  /* 
  loading: Tracks whether a RevenueCat operation is in progress
  offering: Subscription plans (collection)
  selectedId: Selected package identifier (NOT offering identifier)
  packages: Array of available packages from the offering
  */
  const loading = ref(false)
  const offering = ref(null)
  const selectedId = ref('$rc_monthly')
  const packages = ref([])
  const premiumActive = ref(false)
  const error = ref(null)

  const selectedPkg = computed(() => {
    const pkg = packages.value.find(p => p.identifier === selectedId.value)
    console.log('[usePurchases] selectedPkg computed:', {
      selectedId: selectedId.value,
      packagesCount: packages.value.length,
      packageIds: packages.value.map(p => p.identifier),
      foundPackage: pkg?.identifier
    })
    return pkg
  })

  async function refreshEntitlement() {
    try {
      const info = await Purchases.getCustomerInfo()
      premiumActive.value = !!info?.entitlements?.active?.premium
      console.log('[usePurchases] Premium active:', premiumActive.value)
      return premiumActive.value
    } catch (e) {
      console.warn('[usePurchases] getCustomerInfo failed', e)
      return false
    }
  }

  async function loadOffering() {
    loading.value = true
    error.value = null

    try {
      const response = await Purchases.getOfferings()

      offering.value = response.current ?? null
      packages.value = offering.value?.availablePackages ?? []

      if (packages.value.length === 0) {
        error.value = 'No subscription packages available'
      }

      await refreshEntitlement()
    } catch (e) {
      console.error('[usePurchases] Failed to load offerings:', e)
      error.value = e?.message || 'Failed to load products'
    } finally {
      loading.value = false
    }
  }

  async function purchaseSelected() {
    if (!selectedPkg.value) {
      error.value = 'Please select a subscription plan'
      return false
    }

    loading.value = true
    error.value = null

    try {
      const { customerInfo } = await Purchases.purchasePackage({
        aPackage: selectedPkg.value
      })

      premiumActive.value = !!customerInfo?.entitlements?.active?.premium
      return premiumActive.value
    } catch (e) {
      if (e?.userCancelled) {
        error.value = 'Purchase cancelled'
      } else {
        error.value = e?.message || 'Purchase failed'
      }
      return false
    } finally {
      loading.value = false
    }
  }

  async function restore() {
    loading.value = true
    error.value = null

    try {
      const info = await Purchases.restorePurchases()
      premiumActive.value = !!info?.entitlements?.active?.premium
      return premiumActive.value
    } catch (e) {
      error.value = e?.message || 'Restore failed'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    // state
    loading,
    error,
    packages,
    selectedId,
    selectedPkg,
    premiumActive,
    offering,
    // actions
    loadOffering,
    purchaseSelected,
    restore,
    refreshEntitlement,
  }
}