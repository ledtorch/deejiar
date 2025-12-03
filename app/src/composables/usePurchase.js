import { ref, computed, toRaw } from 'vue'
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
  const selectedId = ref('$rc_annual')
  const packages = ref([])
  const isPremium = ref(false)
  const error = ref(null)

  const selectedPkg = computed(() => {
    return packages.value.find(p => p.identifier === selectedId.value)
  })

  async function refreshEntitlement() {
    try {
      const info = await Purchases.getCustomerInfo()
      isPremium.value = !!info?.customerInfo?.entitlements?.active?.premium
      return isPremium.value
    } catch (e) {
      return false
    }
  }

  async function loadOffering() {
    loading.value = true
    error.value = null

    try {
      console.log('📡 Calling Purchases.getOfferings()...')
      const response = await Purchases.getOfferings()

      // ✅ Log the RAW response
      console.log('📦 RAW Response:', JSON.stringify(response, null, 2))
      console.log('📦 response.current:', response.current)
      console.log('📦 response.all:', response.all)

      offering.value = response.current ?? null

      if (offering.value) {
        console.log('📦 offering.availablePackages:', offering.value.availablePackages)
        packages.value = offering.value.availablePackages ?? []
      } else {
        console.warn('⚠️ No current offering found!')
        packages.value = []
      }

      console.log('📦 Final packages.value length:', packages.value.length)

      if (packages.value.length === 0) {
        error.value = 'No subscription packages available'
        console.error('❌ No packages loaded!')
      } else {
        console.log('✅ Packages loaded successfully:')
        packages.value.forEach(pkg => {
          console.log(`  - ${pkg.identifier}: ${pkg.product?.priceString}`)
        })
      }

      await refreshEntitlement()
    } catch (e) {
      console.error('❌ loadOffering error:', e)
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
      const rawPackage = toRaw(selectedPkg.value)

      const result = await Purchases.purchasePackage({
        aPackage: rawPackage
      })

      isPremium.value = !!result.customerInfo?.entitlements?.active?.premium

      return isPremium.value
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

      isPremium.value = !!info?.customerInfo?.entitlements?.active?.premium
      return isPremium.value
    } catch (e) {
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
    isPremium,
    offering,
    loadOffering,
    purchaseSelected,
    restore,
    refreshEntitlement,
  }
}