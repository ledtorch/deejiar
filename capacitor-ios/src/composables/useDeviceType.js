import { ref, onMounted } from 'vue'
import { Capacitor } from '@capacitor/core'

export const useDeviceType = () => {
  const isIPhone = ref(false)
  const isIPad = ref(false)
  const isWeb = ref(false)

  onMounted(() => {

    const ua = navigator.userAgent

    // iPad detection (includes iPadOS 13+ which reports as Mac)
    isIPad.value = /iPad/.test(ua) ||
      (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)

    // iPhone detection
    isIPhone.value = /iPhone/.test(ua)

    // Web = not native
    isWeb.value = !Capacitor.isNativePlatform()
  })

  return { isIPhone, isIPad, isWeb }
}