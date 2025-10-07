// useUserLocation.js
// Unified native/web geolocation with ZERO use of navigator.geolocation on native.
// - On iOS/Android (Capacitor): uses @capacitor/geolocation (native permission dialog).
// - On Web: falls back to navigator.geolocation (browser permission).

import { reactive, ref } from 'vue'
import { Capacitor } from '@capacitor/core'
import { Geolocation } from '@capacitor/geolocation'

export function useUserLocation() {
  const isNative = ref(Capacitor.isNativePlatform())

  const userPosition = reactive({
    latitude: null,
    longitude: null,
    accuracy: null,
    heading: null,
    speed: null,
    timestamp: null
  })

  const hasPermission = ref(false)

  // Native watcher id (Capacitor) or browser watcher id
  let nativeWatchId = null
  let webWatchId = null

  const updateFromCoords = (coords) => {
    userPosition.latitude = coords.latitude ?? userPosition.latitude
    userPosition.longitude = coords.longitude ?? userPosition.longitude
    userPosition.accuracy = coords.accuracy ?? userPosition.accuracy
    userPosition.heading = coords.heading ?? userPosition.heading
    userPosition.speed = coords.speed ?? userPosition.speed
    userPosition.timestamp = Date.now()
  }

  const initialize = async () => {
    if (isNative.value) {
      // Request iOS/Android native location permission
      try {
        const perm = await Geolocation.requestPermissions()
        // iOS returns { location: 'granted' | 'denied' | 'prompt' }
        // Android returns { location: 'granted' | 'denied' }
        hasPermission.value = perm?.location === 'granted'
      } catch (e) {
        console.error('Geolocation permission error (native):', e)
        hasPermission.value = false
      }
    } else {
      // On web, we'll let Mapbox's GeolocateControl trigger the prompt.
      // We still mark as "allowed to try"; the actual permission is handled by the control.
      hasPermission.value = true
    }
  }

  const startWatching = async () => {
    if (isNative.value) {
      if (!hasPermission.value) return
      // Start native watch
      nativeWatchId = await Geolocation.watchPosition(
        { enableHighAccuracy: true, timeout: 10_000, maximumAge: 5_000 },
        (position, err) => {
          if (err) {
            console.error('Native watchPosition error:', err)
            return
          }
          if (position?.coords) updateFromCoords(position.coords)
        }
      )
    } else {
      // WEB fallback (if you need it outside of the Mapbox control).
      // For our Map.vue we don't call this automatically—Mapbox control handles it.
      if ('geolocation' in navigator) {
        webWatchId = navigator.geolocation.watchPosition(
          (pos) => updateFromCoords(pos.coords),
          (error) => console.error('Web watchPosition error:', error),
          { enableHighAccuracy: true, timeout: 10_000, maximumAge: 5_000 }
        )
      }
    }
  }

  const stopWatching = async () => {
    if (isNative.value) {
      if (nativeWatchId != null) {
        try {
          await Geolocation.clearWatch({ id: nativeWatchId })
        } catch (e) {
          console.warn('clearWatch (native) warning:', e)
        }
        nativeWatchId = null
      }
    } else {
      if (webWatchId != null && 'geolocation' in navigator) {
        navigator.geolocation.clearWatch(webWatchId)
        webWatchId = null
      }
    }
  }

  const getPositionForMap = () => {
    if (userPosition.longitude && userPosition.latitude) {
      return [userPosition.longitude, userPosition.latitude]
    }
    // Taipei 101 fallback (lng, lat)
    return [121.56456012803592, 25.034029946192703]
  }

  return {
    // state
    isNative,
    hasPermission,
    userPosition,
    // actions
    initialize,
    startWatching,
    stopWatching,
    // helpers
    getPositionForMap
  }
}