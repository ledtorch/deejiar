import { ref, computed } from 'vue'
import { Capacitor } from '@capacitor/core'
import { AppTrackingTransparency } from 'capacitor-plugin-app-tracking-transparency'

/**
 * useATT - Vue 3 Composable for App Tracking Transparency
 * Using official capacitor-plugin-app-tracking-transparency
 * 
 * Works only on iOS - returns mock data on web/Android
 */
export function useATT() {
  // State
  const status = ref(null)
  const statusName = ref('notDetermined')
  const isLoading = ref(false)
  const error = ref(null)

  // Computed
  const canTrack = computed(() => statusName.value === 'authorized')
  const isNotDetermined = computed(() => statusName.value === 'notDetermined')
  const isDenied = computed(() => statusName.value === 'denied')
  const isRestricted = computed(() => statusName.value === 'restricted')
  const shouldShowPrompt = computed(() => isNotDetermined.value && Capacitor.getPlatform() === 'ios')

  /**
   * Check if running on iOS
   */
  const isIOS = () => {
    return Capacitor.getPlatform() === 'ios'
  }

  /**
   * Get current ATT status without showing prompt
   * 
   * @returns {Promise<Object>} Status object with 'status' property
   * Status values: 'notDetermined' | 'restricted' | 'denied' | 'authorized'
   */
  const getStatus = async () => {
    if (!isIOS()) {
      // Web/Android: Return authorized by default
      statusName.value = 'authorized'
      status.value = 3
      return { status: 'authorized', canTrack: true }
    }

    try {
      isLoading.value = true
      error.value = null

      // Call official plugin
      const result = await AppTrackingTransparency.getStatus()

      // Update state
      statusName.value = result.status

      // Map status to numeric value (for compatibility)
      status.value = result.status === 'authorized' ? 3 :
        result.status === 'denied' ? 2 :
          result.status === 'restricted' ? 1 : 0

      console.log('[ATT] Current status:', result.status)

      return {
        status: result.status,
        canTrack: result.status === 'authorized'
      }
    } catch (err) {
      error.value = err.message || 'Failed to get ATT status'
      console.error('[ATT] Error getting status:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Request ATT permission - Shows system popup
   * IMPORTANT: Call this only after showing custom pre-prompt!
   * 
   * @returns {Promise<Object>} Status object with 'status' property
   */
  const requestPermission = async () => {
    if (!isIOS()) {
      console.log('[ATT] Not on iOS, skipping ATT request')
      return { status: 'authorized', canTrack: true }
    }

    try {
      isLoading.value = true
      error.value = null

      // Check current status first
      const currentStatus = await AppTrackingTransparency.getStatus()

      // If already determined, don't request again
      if (currentStatus.status !== 'notDetermined') {
        console.log('[ATT] Already determined:', currentStatus.status)
        statusName.value = currentStatus.status
        status.value = currentStatus.status === 'authorized' ? 3 :
          currentStatus.status === 'denied' ? 2 :
            currentStatus.status === 'restricted' ? 1 : 0

        return {
          status: currentStatus.status,
          canTrack: currentStatus.status === 'authorized',
          alreadyDetermined: true
        }
      }

      // Request permission - this shows the system popup
      const result = await AppTrackingTransparency.requestPermission()

      // Update state
      statusName.value = result.status
      status.value = result.status === 'authorized' ? 3 :
        result.status === 'denied' ? 2 :
          result.status === 'restricted' ? 1 : 0

      // Log result for debugging
      console.log('[ATT] Permission result:', {
        status: result.status,
        canTrack: result.status === 'authorized'
      })

      return {
        status: result.status,
        canTrack: result.status === 'authorized',
        alreadyDetermined: false
      }
    } catch (err) {
      error.value = err.message || 'Failed to request ATT permission'
      console.error('[ATT] Error requesting permission:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Check if we should initialize analytics
   * Convenience method that checks status and returns boolean
   * 
   * @returns {Promise<boolean>} True if tracking is authorized
   */
  const shouldInitializeTracking = async () => {
    await getStatus()
    return canTrack.value
  }

  return {
    // State
    status,
    statusName,
    isLoading,
    error,

    // Computed
    canTrack,
    isNotDetermined,
    isDenied,
    isRestricted,
    shouldShowPrompt,

    // Methods
    isIOS,
    getStatus,
    requestPermission,
    shouldInitializeTracking
  }
}