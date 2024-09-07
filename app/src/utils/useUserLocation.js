import { reactive } from 'vue';

export function useUserLocation() {
  const userPosition = reactive({
    latitude: null,
    longitude: null
  });

  let watchId = null;

  const updateUserPosition = (position) => {
    userPosition.latitude = position.coords.latitude;
    userPosition.longitude = position.coords.longitude;
    console.log("📍 Updated user position: ", userPosition);
  };

  const startWatching = () => {
    if ('geolocation' in navigator) {
      watchId = navigator.geolocation.watchPosition(
        updateUserPosition,
        (error) => {
          console.error("Error watching position:", error);
        },
        {
          // Use less accurate but more efficient positioning
          enableHighAccuracy: false,
          // Update every 60 seconds
          timeout: 60000,
          // Accept positions up to 3 minutes old
          maximumAge: 180000,
        }
      );
    }
  };

  const stopWatching = () => {
    if (watchId !== null) {
      navigator.geolocation.clearWatch(watchId);
      watchId = null;
    }
  };

  return {
    userPosition,
    updateUserPosition,
    startWatching,
    stopWatching
  };
}