<template>
  <div>
    <div id="map"></div>
    <Locate id="button-locate" @locate="locateUser" aria-label="locate user" />
    <BottomSheet id="bottomsheet" :store="mapStore.selectedStore" @reset="resetSelectedStore" ref="bottomSheetRef" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue';
import { useUserLocation } from '@/composables/useUserLocation.js';
import { useMapStore } from '@/stores/mapStore.js';
import BottomSheet from "../components/theSheet/BottomSheet.vue";
import Locate from "../components/button/Icon/Locate.vue";

const map = ref(null);
const mapboxgl = ref(null);
const tempMarker = ref(null);
const userLocationControl = ref(null); // Web-only
const bottomSheetRef = ref(null);

const {
  isNative,
  initialize,
  startWatching,
  stopWatching,
  hasPermission,
  userPosition,
  getPositionForMap
} = useUserLocation();
const mapStore = useMapStore();

// Locate user
const locateUser = () => {
  // Recenter using latest native/web position (no browser prompt on native)
  if (userPosition.latitude && userPosition.longitude && map.value) {
    map.value.flyTo({
      center: [userPosition.longitude, userPosition.latitude],
      zoom: 15,
      speed: 2,
      curve: 1
    });
  } else if (!isNative.value && userLocationControl.value) {
    // On web, allow Mapbox control to request browser geolocation
    userLocationControl.value.trigger();
    // // 🐞 Debug console
    // console.log("📍 Fly to user position: ", userPosition);
  }
}

// Navigate to location
watch(() => mapStore.navigateToLocation.value, (navigationData) => {
  if (navigationData && navigationData.coordinates && navigationData.zoomLevel && map.value) {
    console.log('🗺️ Store navigation triggered:', navigationData)

    map.value.flyTo({
      center: navigationData.coordinates,
      zoom: navigationData.zoomLevel,
      speed: 2,
      curve: 1
    })

    // Optional: Clear the navigation data after use
    mapStore.navigateToLocation.value = {
      coordinates: null,
      zoomLevel: null
    }
  }
}, { deep: true })

// Reset selected store
const resetSelectedStore = () => {
  // Clear selected store data
  mapStore.resetSelectedStore()

  // remove marker and its data
  if (tempMarker.value) {
    tempMarker.value.remove();
    tempMarker.value = null;
  }
};

// Render stores logic
const updateMapData = (newData) => {
  if (!map.value || !newData) return;

  console.log('🗺️ Updating map with new data:', mapStore.currentDataSource);

  // Remove existing source and layer if they exist
  if (map.value.getSource('stores')) {
    map.value.removeLayer('stores');
    map.value.removeSource('stores');
  }

  // Add new source
  map.value.addSource("stores", {
    type: "geojson",
    data: newData
  });

  // Load marker images for new features
  newData.features.forEach(feature => {
    ["mini", "default", "active"].forEach(size => {
      const iconPath = `/button/marker/${feature.properties.type}-${size}.png`;
      const imageName = feature.properties.title + "-" + size;

      // Check if image already exists to avoid duplicate loading
      if (!map.value.hasImage(imageName)) {
        map.value.loadImage(iconPath, (error, image) => {
          if (error) {
            console.warn(`Failed to load marker image: ${iconPath}`, error);
            return;
          }
          map.value.addImage(imageName, image);
        });
      }
    });
  });

  // Re-add the layer
  map.value.addLayer({
    id: "stores",
    type: "symbol",
    source: "stores",
    layout: {
      "icon-image": [
        "step",
        ["zoom"],
        "",
        10, ["concat", ["get", "title"], "-mini"],
        12.4, ["concat", ["get", "title"], "-default"]
      ],
      "icon-size": 0.25,
      "text-font": ["Geist", "Arial Unicode MS Bold"],
      "text-field": ["step", ["zoom"], "", 13.5, ["get", "title"]],
      "text-anchor": "left"
    },
    paint: {
      "text-color": "#FFFFFF"
    }
  });

  // Re-attach click handlers
  map.value.off("click", "stores", clickMarker); // Remove old handler
  map.value.on("click", "stores", event => clickMarker(event));
};

// Watch for changes in map data
watch(() => mapStore.mapData, (newData) => {
  if (newData) {
    updateMapData(newData);
  }
}, { deep: true });

// Initial stores setup
const initializeStores = async () => {
  try {
    await mapStore.initialize();

    if (mapStore.mapData) {
      updateMapData(mapStore.mapData);

      // Setup zoom listener
      map.value.on("zoom", () => {
        const zoomLevel = map.value.getZoom();

        if (zoomLevel >= 14.5) {
          map.value.setLayoutProperty("stores", "text-offset", [1, 0]);
        } else if (zoomLevel >= 12.4) {
          map.value.setLayoutProperty("stores", "text-offset", [0.8, 0]);
        } else {
          map.value.setLayoutProperty("stores", "text-offset", [0, 0]);
        }
      });

      // Setup click away handler
      map.value.on("click", event => {
        const features = map.value.queryRenderedFeatures(event.point, {
          layers: ["stores"]
        });

        if (!features.length && tempMarker.value) {
          tempMarker.value.remove();
          tempMarker.value = null;
        }
      });
    }
  } catch (error) {
    console.error('Failed to initialize stores:', error);
  }
};

// Click marker
const clickMarker = (event) => {
  // Initialize map
  if (tempMarker.value) {
    tempMarker.value.remove();
  }

  const feature = event.features ? event.features[0] : event;
  const coordinates = feature.geometry.coordinates;
  const type = feature.properties.type;
  const activeIcon = `/button/marker/${type}-active.png`;

  // Store the properties of clicked store and pass to BottomSheet
  mapStore.selectStore(feature.properties);
  mapStore.showMarker = true;

  const el = document.createElement("div");
  el.className = "marker-active";
  el.style.backgroundImage = `url(${activeIcon})`;
  el.style.backgroundPosition = "center";
  el.style.backgroundRepeat = "no-repeat";
  el.style.backgroundSize = "contain";
  el.style.width = "52px";
  el.style.height = "79px";

  tempMarker.value = new mapboxgl.value.Marker(el, { offset: [0, -24] })
    .setLngLat(coordinates)
    .addTo(map.value);

  map.value.flyTo({
    center: [coordinates[0], coordinates[1]],
    offset: [0, -200],
    duration: 500,
    curve: 1
  });

  // Save store marker position
  localStorage.setItem('markerLatitude', coordinates[0]);
  localStorage.setItem('markerLongitude', coordinates[1]);
};

// Execute clickmarker action through mapStore
watch(() => mapStore.selectedStore, (storeData) => {
  if (storeData && mapStore.showMarker && storeData.longitude) {
    console.log('🏪 Creating marker for search result:', storeData.title)

    // Remove existing marker
    if (tempMarker.value) {
      tempMarker.value.remove();
    }

    // Create marker with search result data
    const coordinates = [parseFloat(storeData.longitude), parseFloat(storeData.latitude)]
    const type = storeData.type
    const activeIcon = `/button/marker/${type}-active.png`

    const el = document.createElement("div")
    el.className = "marker-active"
    el.style.backgroundImage = `url(${activeIcon})`
    el.style.backgroundPosition = "center"
    el.style.backgroundRepeat = "no-repeat"
    el.style.backgroundSize = "contain"
    el.style.width = "52px"
    el.style.height = "79px"

    tempMarker.value = new mapboxgl.value.Marker(el, { offset: [0, -24] })
      .setLngLat(coordinates)
      .addTo(map.value)

    map.value.flyTo({
      center: [coordinates[0], coordinates[1]],
      offset: [0, -200],
      duration: 500,
      curve: 1
    });

    localStorage.setItem('markerLatitude', coordinates[0])
    localStorage.setItem('markerLongitude', coordinates[1])
    console.log('Marker created for:', storeData.title)
    console.log('coordinates:', coordinates)
  }
}, { deep: true })

/* -------------------- Custom user-location (no browser prompt on native) -------------------- */

const addUserLocationLayers = () => {
  if (!map.value) return
  if (!map.value.getSource('user-location')) {
    map.value.addSource('user-location', {
      type: 'geojson',
      data: {
        type: 'Feature',
        geometry: { type: 'Point', coordinates: [0, 0] },
        properties: { accuracy: 0, radiusPx: 12 }
      }
    })
  }

  if (!map.value.getLayer('user-accuracy')) {
    map.value.addLayer({
      id: 'user-accuracy',
      type: 'circle',
      source: 'user-location',
      paint: {
        'circle-radius': [
          'coalesce',
          ['to-number', ['get', 'radiusPx']],
          0
        ],
        'circle-color': '#ffffff',
        'circle-opacity': 0.12
      }
    })
  }

  if (!map.value.getLayer('user-dot')) {
    map.value.addLayer({
      id: 'user-dot',
      type: 'circle',
      source: 'user-location',
      paint: {
        'circle-radius': ['interpolate', ['linear'], ['zoom'], 0, 4, 22, 12],
        'circle-color': '#ffffff'
      }
    })
  }
}

const syncUserLocationToMap = () => {
  if (!map.value) return
  const src = map.value.getSource('user-location')
  if (!src) return
  if (!userPosition.latitude || !userPosition.longitude) return

  src.setData({
    type: 'Feature',
    geometry: { type: 'Point', coordinates: [userPosition.longitude, userPosition.latitude] },
    properties: { accuracy: userPosition.accuracy || 0 }
  })
}

// Keep the dot/ring updated
watch(
  () => [userPosition.latitude, userPosition.longitude, userPosition.accuracy],
  () => syncUserLocationToMap()
)

/* -------------------- Map init -------------------- */

onMounted(async () => {
  // Initialize mapboxgl
  await import('mapbox-gl/dist/mapbox-gl.css');
  mapboxgl.value = (await import("mapbox-gl")).default;
  mapboxgl.value.accessToken = import.meta.env.VITE_MAPBOX_TOKEN;

  // Initialize map canvas
  map.value = new mapboxgl.value.Map({
    container: "map",
    style: "mapbox://styles/naivebara/clkyvh09v00m701me403i1svm",
    zoom: 12.5,
    minZoom: 4,
    maxZoom: 18
  })

  map.value.on('load', async () => {
    // Stores and interactions
    initializeStores()

    // User location layers (our own, on all platforms; they don't request perms)
    addUserLocationLayers()

    // Platform-specific geolocation behavior
    if (isNative.value) {
      // Ask ONLY iOS/Android (native) for location
      await initialize()
      if (hasPermission.value) {
        await startWatching()
        // Center to first good fix (fallback to Taipei 101 if not ready)
        const [lng, lat] = getPositionForMap()
        map.value.jumpTo({ center: [lng, lat], zoom: Math.max(map.value.getZoom(), 14) })
        syncUserLocationToMap()
      } else {
        // Fallback: Taipei 101
        map.value.setCenter([121.56456012803592, 25.034029946192703])
      }
    } else {
      // WEB: Keep Mapbox's GeolocateControl
      userLocationControl.value = new mapboxgl.value.GeolocateControl({
        positionOptions: {
          enableHighAccuracy: true
        },
        trackUserLocation: true,
        showUserLocation: true,
        showUserHeading: false
      });

      map.value.addControl(userLocationControl.value);

      // Optionally center via control (triggers browser prompt only on web)
      // We do NOT call navigator.geolocation ourselves.
      nextTick(() => userLocationControl.value?.trigger?.())
    }

    // Map center logic
    // Get stored marker position
    const markerLatitude = localStorage.getItem('markerLatitude');
    const markerLongitude = localStorage.getItem('markerLongitude');
    if (markerLatitude && markerLongitude) {
      map.value.setCenter([
        markerLatitude,
        markerLongitude
      ]);
    }
  })
})

onUnmounted(async () => {
  await stopWatching();
  if (map.value && userLocationControl.value) {
    map.value.removeControl(userLocationControl.value);
    userLocationControl.value = null;
  }
});
</script>

<style lang="scss" scoped>
#map {
  position: relative;
  overflow: hidden;
  width: 100vw;
  height: 100vh;
}

#bottomsheet {
  position: absolute;
  bottom: 0;
  z-index: 1;
  width: 100%;
  height: auto;

  /* Safe area */
  padding-bottom: calc(60px + env(safe-area-inset-bottom));
}

#button-locate {
  position: absolute;
  right: 16px;
  bottom: calc(76px + env(safe-area-inset-bottom));
  z-index: 1;
  transition: transform 0.3s ease;
}

.marker-active {
  background: no-repeat center/contain;
  background-color: aliceblue;
}
</style>