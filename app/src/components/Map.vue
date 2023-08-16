<template>
  <div>
    <div id="map"></div>
    <IconButtonLocate
      id="iconbuttonlocate"
      :state="buttonState"
      @locate="locateUser"
    ></IconButtonLocate>
    <BottomSheet
      id="bottomsheet"
      :store="selectedStore"
      @reset="resetSelectedStore"
    />
  </div>
</template>

<script>
import mapboxgl from "mapbox-gl";
import BottomSheet from "./BottomSheet.vue";
import IconButtonLocate from "./Button/IconButtonLocate.vue";

export default {
  components: {
    BottomSheet,
    IconButtonLocate,
  },
  data() {
    return {
      map: null,
      selectedStore: null,
      buttonState: "default",
      locate: null,
    };
  },

  // ↓ Mount Mapbox
  mounted() {
    mapboxgl.accessToken =
      "pk.eyJ1IjoibmFpdmViYXJhIiwiYSI6ImNsa3lzZmV6ZzA1NHMzbW13ZjJ4aTJodzIifQ.kaC5YvO-g5idBZK4bDvZ7g";

    this.locate = new mapboxgl.GeolocateControl({
      positionOptions: { enableHighAccuracy: true },
      trackUserLocation: true,
      showUserHeading: true,
    });

    navigator.geolocation.getCurrentPosition(
      (position) => {
        this.map.setCenter([
          position.coords.longitude,
          position.coords.latitude,
        ]);
        console.log(
          "🧭 User's current position: " +
            "(" +
            position.coords.latitude +
            "," +
            position.coords.longitude +
            ")"
        );
      },
      (error) => {
        console.error("Geolocation error: ", error);
        this.map.setCenter([-77.0364976166554, 38.897684621644885]); // White House or default location
      }
    );

    this.map = new mapboxgl.Map({
      container: "map",
      style: "mapbox://styles/naivebara/clkyvh09v00m701me403i1svm",
      center: [-77.0364976166554, 38.897684621644885], // White House
      zoom: 12.5,
      minZoom: 3,
      maxZoom: 18,
    });

    this.map.on("load", () => {
      this.addMarkers();
    });
  },

  methods: {
    addMarkers() {
      fetch("/stores.json")
        .then((response) => response.json())
        .then((data) => {
          this.map.addSource("points", {
            type: "geojson",
            data: data,
          });
          // Define the source

          data.features.forEach((feature) => {
            ["mini", "default", "larger", "active"].forEach((size) => {
              const iconPath =
                "/Button/Marker/" +
                feature.properties.type +
                "_" +
                size +
                ".png";
              this.map.loadImage(iconPath, (error, image) => {
                if (error) throw error;
                this.map.addImage(feature.properties.title + "-" + size, image);
                console.log(feature.properties.title + "-" + size);
                console.log(
                  "Marker's Icon:",
                  feature.properties.type + "_" + size + ".png"
                );
              });
            });
          });

          this.map.on("zoom", () => {
            const zoomLevel = this.map.getZoom();

            if (zoomLevel >= 14.5) {
              this.map.setLayoutProperty("points", "text-offset", [1, 0]);
            } else if (zoomLevel >= 12.4) {
              this.map.setLayoutProperty("points", "text-offset", [0.8, 0]);
            } else {
              this.map.setLayoutProperty("points", "text-offset", [0, 0]);
            }
          });

          this.map.addLayer({
            id: "points",
            type: "symbol",
            source: "points",
            layout: {
              "icon-image": [
                "step",
                ["zoom"],
                "", // this will display nothing from zoom levels 3-10
                10,
                ["concat", ["get", "title"], "-mini"],
                12.4,
                ["concat", ["get", "title"], "-default"],
                14.5,
                ["concat", ["get", "title"], "-larger"],
              ],
              "icon-size": 0.25,
              // Import higher resolution and compress to normal size

              "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],

              "text-field": ["step", ["zoom"], "", 13.5, ["get", "title"]],
              // "text-offset": [0, 0],
              "text-anchor": "left",
            },
            paint: {
              "text-color": "#FFFFFF", // Red color for example
            },
          });

          this.map.on("click", "points", (e) => {
            console.log("✅ Clicked the Marker");
            const title = e.features[0].properties.title;
            this.selectedStore = data.features.find(
              (store) => store.properties.title === title
            ).properties;

            console.log("📃 Selected Store:", this.selectedStore);
            // Check the data passed by the click
          });
        });
    },

    locateUser() {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          this.map.flyTo({
            center: [position.coords.longitude, position.coords.latitude],
            zoom: 12.5, // optional zoom level
            speed: 2, // make the flying slow
            curve: 1, // change the speed at which it zooms out
          });
          console.log(
            "🧭 Locate the user to current position: " +
              "(" +
              position.coords.latitude +
              "," +
              position.coords.longitude +
              ")"
          );
        },
        (error) => {
          console.error("Geolocation error: ", error);
          this.map.setCenter([-77.0364976166554, 38.897684621644885]); // White House or default location
        }
      );
    },

    resetSelectedStore() {
      this.selectedStore = null;
    },
    // Clean the data and make showAvatar = false, so the default avatar could be displayed
  },
};
</script>

<style>
#map {
  position: relative;
  display: flex;
  flex-direction: column; /* Align children vertically */
  width: 100vw;
  height: 100vh;
  overflow: hidden; /* Prevent any unexpected overflow */
}

#bottomsheet {
  position: absolute;
  bottom: 0;
  z-index: 1;
  width: 100%;
  height: auto;
}

#iconbuttonlocate {
  position: absolute;
  bottom: 48px; /* Distance from the bottom */
  right: 16px; /* Distance from the right */
  z-index: 1;
  transition: transform 0.3s ease;
}
</style>
