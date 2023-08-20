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
import BottomSheet from "./Sheet/BottomSheet.vue";
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
      mapData: null, // Register the data for the fn' outside addMarkers
      tempMarker: null, // Register the temporary marker
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
      minZoom: 4,
      maxZoom: 18,
    });

    this.map.on("load", () => {
      this.addMarkers();
    });
  },

  methods: {
    // ↓ Marker
    addMarkers() {
      fetch("/stores.json")
        .then((response) => response.json())
        .then((data) => {
          this.map.addSource("points", {
            type: "geojson",
            data: data,
          });
          this.mapData = data;
          // Define the source

          // ↓ Extract the data from json
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
                // // ↓ 🐞 Debug console
                // console.log(
                //   "Marker's Icon:",
                //   feature.properties.type + "_" + size + ".png"
                // );
              });
            });
          });

          // ↓ Setup the text of the marker
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

          // ↓ Render the marker as a layer
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

          // Pass the data to clickMarker
          this.map.on("click", "points", (event) => this.clickMarker(event));

          // If click the map, reset the active marker
          this.map.on("click", (event) => {
            // Check if the click event occurred on the points layer
            const features = this.map.queryRenderedFeatures(event.point, {
              layers: ["points"], // assuming "points" is the layer id where markers are
            });

            // If the click event did not occur on the points layer, remove the temporary marker
            if (!features.length && this.tempMarker) {
              this.tempMarker.remove();
              this.tempMarker = null; // Reset the temporary marker variable
            }
          });
        });
    },

    // ↓ Create a temp marker and move the center when click it
    clickMarker(event) {
      if (this.tempMarker) {
        this.tempMarker.remove();
      }

      const title = event.features[0].properties.title;
      // When the event pass to clickMarker(), the Mapbox makes a new "features" that packages the data of the event
      // Which means this "features" is a new features instead of the stores.json
      const coordinates = event.features[0].geometry.coordinates;
      const iconString = event.features[0].properties.icon;
      const iconObject = JSON.parse(iconString);
      const activeIcon = iconObject.active;

      this.selectedStore = this.mapData.features.find(
        (store) => store.properties.title === title
      ).properties;

      // ↓ Create a temporary marker
      const el = document.createElement("div");
      el.className = "marker-active";
      el.style.backgroundImage = `url(${activeIcon})`;
      el.style.backgroundPosition = "center";
      el.style.backgroundRepeat = "no-repeat";
      el.style.backgroundSize = "contain";
      el.style.width = "52px";
      el.style.height = "79px";

      console.log("Icon: ", activeIcon);

      // console.log("el.style.backgroundImage: " + el.style.backgroundImage);
      this.tempMarker = new mapboxgl.Marker(el, { offset: [0, -24] })
        .setLngLat(coordinates)
        .addTo(this.map);

      this.map.flyTo({
        center: [coordinates[0], coordinates[1]],
        offset: [0, -200],
        duration: 500,
        curve: 1,
      });
      console.log("center: " + coordinates[0] + ", " + coordinates[1]);

      // // ↓ 🐞 Debug console
      // console.log("⬇️ Clicked the Marker");
      // console.log("title: " + title);
      // console.log("Selected Store:", this.selectedStore);
    },

    // ↓ Locate
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
      this.tempMarker.remove();
    },
    // Clean the data and make showAvatar = false, so the default avatar could be displayed
  },
};
</script>

<style scoped>
#map {
  position: relative;
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

.marker-active {
  background: no-repeat center/contain;
  background-color: aliceblue;
}
</style>
