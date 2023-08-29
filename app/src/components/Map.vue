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
// What?
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
      storeData: null, // Register the data for the fn' outside addStores
      districtData: null, // Register the data for the fn' outside addStores
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
        const el = document.createElement("div");
        el.className = "location-indicator";

        const ringDiv = document.createElement("div");
        ringDiv.className = "ring";
        el.appendChild(ringDiv);

        const innerBallDiv = document.createElement("div");
        innerBallDiv.className = "inner-ball";
        ringDiv.appendChild(innerBallDiv);

        new mapboxgl.Marker(el)
          .setLngLat([position.coords.longitude, position.coords.latitude])
          .addTo(this.map);
        // Create a location indicator of the user

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
      this.addStores();
      this.addDistricts();
    });
  },

  methods: {
    // ↓ Stores
    addStores() {
      fetch("/stores.json")
        .then((response) => response.json())
        .then((data) => {
          this.map.addSource("stores", {
            type: "geojson",
            data: data,
          });
          this.storeData = data;
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

          // ↓ Setup the text of the stores' marker
          this.map.on("zoom", () => {
            const zoomLevel = this.map.getZoom();

            if (zoomLevel >= 14.5) {
              this.map.setLayoutProperty("stores", "text-offset", [1, 0]);
            } else if (zoomLevel >= 12.4) {
              this.map.setLayoutProperty("stores", "text-offset", [0.8, 0]);
            } else {
              this.map.setLayoutProperty("stores", "text-offset", [0, 0]);
            }
          });

          // ↓ Render the stores' marker as a layer
          this.map.addLayer({
            id: "stores",
            type: "symbol",
            source: "stores",
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
              "text-anchor": "left",
            },
            paint: {
              "text-color": "#FFFFFF",
            },
          });

          // Pass the data to clickMarker
          this.map.on("click", "stores", (event) => this.clickMarker(event));

          // If click the map, reset the active stores' marker
          this.map.on("click", (event) => {
            // Check if the click event occurred on the stores layer
            const features = this.map.queryRenderedFeatures(event.point, {
              layers: ["stores"], // assuming "stores" is the layer id where markers are
            });

            // If the click event did not occur on the stores layer, remove the temporary marker
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

      this.selectedStore = this.storeData.features.find(
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

    // ↓ District
    addDistricts() {
      fetch("/districts.json")
        .then((response) => response.json())
        .then((data) => {
          this.map.addSource("districts", {
            type: "geojson",
            data: data,
          });
          this.districtData = data;

          // Render the district's area
          this.map.addLayer({
            id: "districts",
            type: "fill",
            source: "districts",
            layout: {},
            paint: {
              "fill-color": "#3DC363",
              "fill-opacity": 0.6,
            },
            filter: ["==", "$type", "Polygon"],
          });
          // Render the district's border
          this.map.addLayer({
            id: "outline",
            type: "line",
            source: "districts",
            layout: {},
            paint: {
              "line-color": "#3DC363",
              "line-width": 1,
            },
            filter: ["==", "$type", "Polygon"],
          });

          // ↓ Extract the data from json
          // Load images
          data.features.forEach((feature) => {
            if (feature.geometry.type === "Point") {
              ["mini", "default", "larger", "active"].forEach((size) => {
                const iconPath =
                  "/Button/Marker/" +
                  feature.properties.type +
                  "_" +
                  size +
                  ".png";
                this.map.loadImage(iconPath, (error, image) => {
                  if (error) throw error;
                  const iconName = feature.properties.type + "-" + size;
                  this.map.addImage(iconName, image);
                });
              });
            }
          });

          // ↓ Setup the text of the districts' marker
          this.map.on("zoom", () => {
            const zoomLevel = this.map.getZoom();

            if (zoomLevel >= 14.5) {
              this.map.setLayoutProperty("markers", "text-offset", [1, 0]);
            } else if (zoomLevel >= 12.4) {
              this.map.setLayoutProperty("markers", "text-offset", [0.8, 0]);
            } else {
              this.map.setLayoutProperty("markers", "text-offset", [0, 0]);
            }
          });

          // Render the districts' marker as a layer
          this.map.addLayer({
            id: "markers",
            type: "symbol",
            source: "districts",
            layout: {
              "icon-image": [
                "step",
                ["zoom"],
                "", // this will display nothing from zoom levels 3-10
                10,
                ["concat", ["get", "type"], "-mini"],
                12.4,
                ["concat", ["get", "type"], "-default"],
                14.5,
                ["concat", ["get", "type"], "-larger"],
              ],
              "icon-size": 0.25,
              "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
              "text-field": ["step", ["zoom"], "", 13.5, ["get", "title"]],
              "text-anchor": "left",
            },
            paint: {
              "text-color": "#FFFFFF",
            },
            filter: ["==", "$type", "Point"],
          });
        });
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

<style lang="scss" scoped>
#map {
  overflow: hidden; /* Prevent any unexpected overflow */
  position: relative;
  flex-direction: column; /* Align children vertically */
  width: 100vw;
  height: 100vh;
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

.location-indicator {
  width: 24px;
  height: 24px;
  padding: 2px;
  display: flex; // Added to center the inner elements
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  z-index: 1;
}

.inner-ball {
  // Corrected from .ball to .inner-ball
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
