// src/composables/usePurchases.js
import { ref, computed } from 'vue'
import { Capacitor } from '@capacitor/core'
import { Purchases } from '@revenuecat/purchases-capacitor'

export function usePurchases() {
  const loading = ref(false)
  const offering = ref(null)
  const selectedId = ref('Monthly') // or 'Yearly' by default
  const packages = ref([])
  const premiumActive = ref(false)
  const error = ref(null)

  const selectedPkg = computed(() =>
    packages.value.find(p => p.identifier === selectedId.value)
  )

  async function refreshEntitlement() {
    try {
      const info = await Purchases.getCustomerInfo()
      premiumActive.value = !!info?.entitlements?.active?.premium
      return premiumActive.value
    } catch (e) {
      console.warn('[RC] getCustomerInfo failed', e)
      return false
    }
  }

  async function loadOffering() {
    if (!Capacitor.isNativePlatform()) return
    loading.value = true
    error.value = null
    try {
      const res = await Purchases.getOfferings()
      // We used one Offering with two Packages you created in RC:
      // Package identifiers: "Monthly" and "Yearly"
      // (from the screen where you added packages to the offering)
      offering.value = res.current ?? null
      packages.value = offering.value?.availablePackages ?? []
      await refreshEntitlement()
    } catch (e) {
      error.value = e?.message || 'Failed to load products'
    } finally {
      loading.value = false
    }
  }

  async function purchaseSelected() {
    if (!selectedPkg.value) return
    loading.value = true
    error.value = null
    try {
      const { customerInfo } = await Purchases.purchasePackage({
        identifier: selectedPkg.value.identifier, // 'Monthly' or 'Yearly'
        offeringIdentifier: offering.value.identifier, // your offering id
      })
      premiumActive.value = !!customerInfo?.entitlements?.active?.premium
      return premiumActive.value
    } catch (e) {
      // Handle user cancels, etc.
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
    loading, error, packages, selectedId, selectedPkg, premiumActive, offering,
    // actions
    loadOffering, purchaseSelected, restore, refreshEntitlement,
  }
}