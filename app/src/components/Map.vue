<template>
  <div>
    <div id="map"></div>
    <PicksByAuthor id="pickscard" @select-bar="handleSelectBar" />
    <Locate id="button-locate" @locate="locateUser" aria-label="locate user" />
    <BottomSheet id="bottomsheet" :store="selectedStore" @reset="resetSelectedStore" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useUserLocation } from '../utils/useUserLocation.js';
import BottomSheet from "./Sheet/BottomSheet.vue";
import Locate from "./Button/Icon/Locate.vue";
import PicksByAuthor from "./Card/PicksByAuthor.vue";

const map = ref(null);
const mapboxgl = ref(null);
const selectedStore = ref(null);
const tempMarker = ref(null);
const userLocationControl = ref(null);

const { userPosition, startWatching, stopWatching } = useUserLocation();

// stores json
let storeData = null;

// Locate user
// const locateUser = () => {
//   if (userLocationControl.value) {
//     console.log("userLocationControl.value: " + userLocationControl.value);
//     userLocationControl.value.trigger();
//   } else {
//     console.log("GeolocateControl not available");
//   }
// };

// // v2
// const locateUser = () => {
//   if (userLocationControl.value) {
//     if (!userLocationControl.value._watchState) {
//       // If not actively watching, trigger the control
//       userLocationControl.value.trigger();
//     } else {
//       // If already watching, center the map on the user's location
//       if (userPosition.latitude && userPosition.longitude) {
//         map.value.flyTo({
//           center: [userPosition.longitude, userPosition.latitude],
//           zoom: 15,
//           speed: 2,
//           curve: 1
//         });
//         userLocationControl.value.trigger();
//       } else {
//         console.log("User position not available yet");
//       }
//     }
//     console.log("GeolocateControl triggered or map centered on user location");
//   } else {
//     console.log("GeolocateControl not available");
//   }
// };

// // v3
// const locateUser = () => {
//   if (userLocationControl.value) {
//     if (userPosition.latitude && userPosition.longitude) {
//       map.value.flyTo({
//         center: [userPosition.longitude, userPosition.latitude],
//         zoom: 15,
//         speed: 2,
//         curve: 1
//       });
//       userLocationControl.value.trigger();
//       console.log("📍 Flying to user position: ", userPosition);
//     } else {
//       userLocationControl.value.trigger();
//       console.log("Triggering GeolocateControl");
//     }
//   } else {
//     console.log("GeolocateControl not available");
//   }
// };

// v4
const locateUser = () => {
  // if (userPosition.latitude && userPosition.longitude) {
  map.value.flyTo({
    center: [userPosition.longitude, userPosition.latitude],
    zoom: 15,
    speed: 2,
    curve: 1
  });
  userLocationControl.value.trigger();
  console.log("📍 Flying to user position: ", userPosition);
  // } else {
  //   userLocationControl.value.trigger();
  //   console.log("Triggering GeolocateControl");
  // }
};

// Reset selected store
const resetSelectedStore = () => {
  // remove marker and its data
  tempMarker.value.remove();
  tempMarker.value = null;

  // remove selected store data
  selectedStore.value = null;
};

// Render stores logic
const addStores = () => {
  const url = `/stores.json?v=${new Date().getTime()}`;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      storeData = data;

      map.value.addSource("stores", {
        type: "geojson",
        data: storeData
      });

      storeData.features.forEach(feature => {
        ["mini", "default", "larger", "active"].forEach(size => {
          const iconPath = `/button/marker/${feature.properties.type}-${size}.png`;
          map.value.loadImage(iconPath, (error, image) => {
            if (error) throw error;
            map.value.addImage(feature.properties.title + "-" + size, image);
          });
        });
      });

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
            12.4, ["concat", ["get", "title"], "-default"],
            14.5, ["concat", ["get", "title"], "-larger"]
          ],
          "icon-size": 0.25,
          "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
          "text-field": ["step", ["zoom"], "", 13.5, ["get", "title"]],
          "text-anchor": "left"
        },
        paint: {
          "text-color": "#FFFFFF"
        }
      });

      map.value.on("click", "stores", event => clickMarker(event));

      map.value.on("click", event => {
        const features = map.value.queryRenderedFeatures(event.point, {
          layers: ["stores"]
        });

        if (!features.length && tempMarker.value) {
          tempMarker.value.remove();
          tempMarker.value = null;
        }
      });
    });
};

// Click marker
const clickMarker = (event) => {
  // Initialize map
  if (tempMarker.value) {
    tempMarker.value.remove();
  }
  hidePicksByAuthor();

  const feature = event.features ? event.features[0] : event;
  const title = feature.properties.title;
  const coordinates = feature.geometry.coordinates;
  const iconString = feature.properties.icon;
  const iconObject = typeof iconString === 'string' ? JSON.parse(iconString) : iconString;
  const activeIcon = iconObject.active;

  selectedStore.value = storeData.features.find(
    store => store.properties.title === title
  ).properties;

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

// PicksByAuthor logic
const handleSelectBar = (bar) => {
  const event = {
    features: [{
      properties: bar.properties,
      geometry: bar.geometry
    }]
  };
  clickMarker(event);
};

const hidePicksByAuthor = () => {
  const picksCard = document.getElementById('pickscard');
  if (picksCard) {
    picksCard.style.display = 'none';
  }
};


// Initialize map
onMounted(async () => {
  // Initialize mapboxgl
  await import('mapbox-gl/dist/mapbox-gl.css');
  mapboxgl.value = (await import("mapbox-gl")).default;
  mapboxgl.value.accessToken = import.meta.env.VITE_MAPBOX_TOKEN;

  // Initialize map canvas
  map.value = new mapboxgl.value.Map({
    container: "map",
    style: "mapbox://styles/naivebara/cluvh6drq000001q11cezdkgl",
    zoom: 12.5,
    minZoom: 4,
    maxZoom: 18
  });

  // Get stored marker position
  const markerLatitude = localStorage.getItem('markerLatitude');
  const markerLongitude = localStorage.getItem('markerLongitude');


  map.value.on("load", () => {
    addStores();

    // Initialize GeolocateControl only if it doesn't exist
    userLocationControl.value = new mapboxgl.value.GeolocateControl({
      positionOptions: {
        enableHighAccuracy: true
      },
      trackUserLocation: true,
      showUserLocation: true,
      showUserHeading: false
    });

    map.value.addControl(userLocationControl.value);

  });

  // Map center logic
  navigator.geolocation.getCurrentPosition(
    // Use stored marker position if available, otherwise use current position
    position => {
      if (markerLatitude && markerLongitude) {
        map.value.setCenter([
          markerLatitude,
          markerLongitude
        ]);
      } else {
        userLocationControl.value.trigger();
      }
      // // 🐞 Debug console
      // console.log(
      //   "📍 User's current position: " +
      //   "(" + position.coords.latitude + "," + position.coords.longitude + ")"
      // );
    },
    // If user denies geolocation, set map center to White House
    error => {
      console.error("Geolocation error: ", error);
      map.value.setCenter([-77.0364976166554, 38.897684621644885]);
    }
  );

  startWatching();
});

onUnmounted(() => {
  stopWatching();
  if (map.value && userLocationControl.value) {
    map.value.removeControl(userLocationControl.value);
    userLocationControl.value = null;
  }
});
</script>

<style lang="scss" scoped>
#map {
  /* Prevent any unexpected overflow */
  overflow: hidden;

  position: relative;
  width: 100vw;
  height: 100vh;
}

#pickscard {
  position: absolute;
  z-index: 1;
  width: 100%;
}

#user-marker {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;
}

#bottomsheet {
  position: absolute;
  bottom: 0;
  z-index: 1;
  width: 100%;
  height: auto;
}

#button-locate {
  position: absolute;
  bottom: 48px;
  right: 16px;
  z-index: 1;
  transition: transform 0.3s ease;
}

.marker-active {
  background: no-repeat center/contain;
  background-color: aliceblue;
}

.location-indicator {
  width: 24px;
  height: 24px;
  padding: 2px;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  z-index: 1;
}

.inner-ball {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  border-radius: 16px;
  background-color: var(--token-theme, #fafafa);
}

.ring {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  border-radius: 20px;
  border: 1px dashed var(--token-theme, #fafafa);
}
</style>