// src/composables/usePurchases.js
import { ref, computed, toRaw } from 'vue'  // ✅ Import toRaw
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
  const selectedId = ref('$rc_annual')  // ✅ Default to annual (yearly)
  const packages = ref([])
  const premiumActive = ref(false)
  const error = ref(null)

  const selectedPkg = computed(() => {
    return packages.value.find(p => p.identifier === selectedId.value)
  })

  async function refreshEntitlement() {
    try {
      console.log('🔄 [RC] Refreshing entitlement...')
      const info = await Purchases.getCustomerInfo()
      console.log('📊 [RC] Customer info:', JSON.stringify(info, null, 2))

      premiumActive.value = !!info?.customerInfo?.entitlements?.active?.premium
      console.log('✅ [RC] Premium active:', premiumActive.value)
      return premiumActive.value
    } catch (e) {
      console.error('❌ [RC] getCustomerInfo failed:', e)
      return false
    }
  }

  async function loadOffering() {
    loading.value = true
    error.value = null

    try {
      console.log('🔄 [RC] Loading offerings...')
      const response = await Purchases.getOfferings()
      console.log('📦 [RC] Offerings response:', JSON.stringify(response, null, 2))

      offering.value = response.current ?? null
      packages.value = offering.value?.availablePackages ?? []

      console.log('📋 [RC] Packages loaded:', packages.value.length)
      packages.value.forEach((pkg, i) => {
        console.log(`  Package ${i + 1}:`, {
          id: pkg.identifier,
          type: pkg.packageType,
          product: pkg.product?.identifier,
          price: pkg.product?.priceString
        })
      })

      if (packages.value.length === 0) {
        error.value = 'No subscription packages available'
      }

      await refreshEntitlement()
    } catch (e) {
      console.error('❌ [RC] Failed to load offerings:', e)
      error.value = e?.message || 'Failed to load products'
    } finally {
      loading.value = false
    }
  }

  async function purchaseSelected() {
    if (!selectedPkg.value) {
      console.error('❌ [RC] No package selected!')
      error.value = 'Please select a subscription plan'
      return false
    }

    loading.value = true
    error.value = null

    try {
      console.log('💳 [RC] Starting purchase...')
      console.log('  Package:', selectedPkg.value.identifier)
      console.log('  Product:', selectedPkg.value.product?.identifier)
      console.log('  Price:', selectedPkg.value.product?.priceString)

      // ✅ FIX: Use toRaw() to get non-reactive object
      const rawPackage = toRaw(selectedPkg.value)
      console.log('📦 [RC] Raw package:', rawPackage)

      const result = await Purchases.purchasePackage({
        aPackage: rawPackage  // ✅ Pass raw, non-reactive object
      })

      console.log('📄 [RC] Purchase result:', JSON.stringify(result, null, 2))

      premiumActive.value = !!result.customerInfo?.entitlements?.active?.premium
      console.log('✅ [RC] Purchase complete! Premium:', premiumActive.value)

      return premiumActive.value
    } catch (e) {
      console.error('❌ [RC] Purchase error:', e)
      console.error('Error details:', JSON.stringify(e, null, 2))

      if (e?.userCancelled) {
        console.log('👤 User cancelled purchase')
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
      console.log('🔄 [RC] Restoring purchases...')
      const info = await Purchases.restorePurchases()
      console.log('📄 [RC] Restore result:', JSON.stringify(info, null, 2))

      premiumActive.value = !!info?.customerInfo?.entitlements?.active?.premium
      console.log('✅ [RC] Restore complete! Premium:', premiumActive.value)
      return premiumActive.value
    } catch (e) {
      console.error('❌ [RC] Restore failed:', e)
      error.value = e?.message || 'Restore failed'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    packages,
    selectedId,
    selectedPkg,
    premiumActive,
    offering,
    loadOffering,
    purchaseSelected,
    restore,
    refreshEntitlement,
  }
}