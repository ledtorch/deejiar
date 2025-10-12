// src/composables/usePurchases.js
import { ref, computed } from 'vue'
import { Capacitor } from '@capacitor/core'
import { Purchases } from '@revenuecat/purchases-capacitor'

export function usePurchases() {
  const loading = ref(false)
  const offering = ref(null)
  const selectedId = ref('Yearly') // Default to Yearly to match UI
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
    if (!Capacitor.isNativePlatform()) {
      console.warn('[usePurchases] Cannot check entitlements on web')
      return false
    }

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
    console.log('[usePurchases] loadOffering called')
    console.log('[usePurchases] Is native platform?', Capacitor.isNativePlatform())

    if (!Capacitor.isNativePlatform()) {
      console.warn('[usePurchases] ⚠️ RevenueCat only works on iOS. Please test on a real device.')
      error.value = 'Subscriptions only available on iOS'
      return
    }

    loading.value = true
    error.value = null

    try {
      console.log('[usePurchases] Fetching offerings from RevenueCat...')
      const res = await Purchases.getOfferings()

      console.log('[usePurchases] Offerings response:', res)

      offering.value = res.current ?? null
      packages.value = offering.value?.availablePackages ?? []

      console.log('[usePurchases] Offering loaded:', {
        offeringId: offering.value?.identifier,
        packagesCount: packages.value.length,
        packageIds: packages.value.map(p => p.identifier)
      })

      if (packages.value.length === 0) {
        console.error('[usePurchases] ❌ No packages found!')
        console.error('[usePurchases] Please check:')
        console.error('[usePurchases] 1. RevenueCat offering is configured')
        console.error('[usePurchases] 2. Offering is set as "current"')
        console.error('[usePurchases] 3. Packages are added to the offering')
        console.error('[usePurchases] 4. You are signed into Apple ID on device')
        error.value = 'No subscription packages available. Please sign into Apple ID or check RevenueCat configuration.'
      }

      await refreshEntitlement()
    } catch (e) {
      console.error('[usePurchases] Failed to load offerings:', e)
      error.value = e?.message || 'Failed to load products'

      if (e?.message?.includes('No active account')) {
        error.value = 'Please sign into Apple ID in Settings → App Store'
      }
    } finally {
      loading.value = false
    }
  }

  async function purchaseSelected() {
    console.log('[usePurchases] purchaseSelected called')
    console.log('[usePurchases] selectedPkg:', selectedPkg.value)

    if (!Capacitor.isNativePlatform()) {
      console.error('[usePurchases] ❌ Purchases only work on iOS')
      error.value = 'Purchases only available on iOS'
      return false
    }

    if (!selectedPkg.value) {
      console.error('[usePurchases] ❌ No package selected!')
      error.value = 'Please select a subscription plan'
      return false
    }

    loading.value = true
    error.value = null

    try {
      console.log('[usePurchases] Starting purchase:', {
        packageId: selectedPkg.value.identifier,
        offeringId: offering.value?.identifier,
        productId: selectedPkg.value.product?.identifier
      })

      const { customerInfo } = await Purchases.purchasePackage({
        identifier: selectedPkg.value.identifier,
        offeringIdentifier: offering.value.identifier,
      })

      premiumActive.value = !!customerInfo?.entitlements?.active?.premium
      console.log('[usePurchases] ✅ Purchase complete. Premium:', premiumActive.value)

      return premiumActive.value
    } catch (e) {
      console.error('[usePurchases] Purchase error:', e)

      if (e?.userCancelled) {
        error.value = 'Purchase cancelled'
        console.log('[usePurchases] User cancelled purchase')
      } else {
        error.value = e?.message || 'Purchase failed'
        console.error('[usePurchases] Purchase failed:', error.value)
      }
      return false
    } finally {
      loading.value = false
    }
  }

  async function restore() {
    console.log('[usePurchases] restore called')

    if (!Capacitor.isNativePlatform()) {
      console.error('[usePurchases] ❌ Restore only works on iOS')
      error.value = 'Restore only available on iOS'
      return false
    }

    loading.value = true
    error.value = null

    try {
      const info = await Purchases.restorePurchases()
      premiumActive.value = !!info?.entitlements?.active?.premium
      console.log('[usePurchases] ✅ Restore complete. Premium:', premiumActive.value)
      return premiumActive.value
    } catch (e) {
      console.error('[usePurchases] Restore failed:', e)
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