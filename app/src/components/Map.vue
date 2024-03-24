<template>
  <div>
    <div id="map"></div>
    <Locate id="button-locate" :state="buttonState" @locate="locateUser" />
    <BottomSheet id="bottomsheet" :store="selectedStore" @reset="resetSelectedStore" />
  </div>
</template>

<script>
import mapboxgl from "mapbox-gl";
import BottomSheet from "./Sheet/BottomSheet.vue";
import Locate from "./Button/Icon/Locate.vue";
import { useRouter } from "vue-router";
import { useHead } from 'unhead';

export default {
  // 🏗️TODO: OG image
  setup() {
    useHead({
      title: 'Deejiar | Map for Taste Adventurers to Explore without Boundaries',
      meta: [
        {
          name: 'description',
          content: 'TīTsia designed by Jerry',
        },
        {
          property: 'og:title',
          content: 'Deejiar | Map for Taste Adventurers to Explore without Boundaries',
        },
        {
          property: 'og:description',
          content: 'This is a page',
        },
        {
          property: 'og:image',
          content: 'https://app.morispace.com/Icon/logo/logo.png',
        },
        {
          property: 'twitter:title',
          content: 'TīTsia',
        },
        {
          property: 'twitter:description',
          content: 'This is a page',
        },
        {
          property: 'twitter:image',
          content: 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Welsh_Pembroke_Corgi.jpg/640px-Welsh_Pembroke_Corgi.jpg',
        },
        {
          name: 'twitter:card',
          content: 'summary_large_image',
        },
        {
          property: 'og:type',
          content: 'website',
        }
      ],
      link: [
        {
          rel: 'icon',
          href: 'https://app.morispace.com/Icon/logo/logo.ico',
          type: 'image/x-icon',
        },
      ]
    })
  },
  components: {
    BottomSheet,
    Locate
  },
  data() {
    return {
      map: null,
      selectedStore: null,
      buttonState: "default",
      locate: null,

      // Register the data for using out of the render layer
      storeData: null,
      districtData: null,

      // Register the temporary marker
      tempMarker: null
    };
  },

  // Mount Mapbox
  mounted() {
    mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN;

    this.locate = new mapboxgl.GeolocateControl({
      positionOptions: { enableHighAccuracy: true },
      trackUserLocation: true,
      showUserHeading: true
    });

    // Initialize stored position
    const markerLatitude = localStorage.getItem('markerLatitude');
    const markerLongitude = localStorage.getItem('markerLongitude');
    console.log("markerLatitude: " + markerLatitude)

    navigator.geolocation.getCurrentPosition(
      position => {
        // TODO: User mark
        // const el = document.createElement("div");
        // el.className = "location-indicator";

        // const ringDiv = document.createElement("div");
        // ringDiv.className = "ring";
        // el.appendChild(ringDiv);

        // const innerBallDiv = document.createElement("div");
        // innerBallDiv.className = "inner-ball";
        // ringDiv.appendChild(innerBallDiv);

        // // Create a location indicator of the user
        // new mapboxgl.Marker(el)
        //   .setLngLat([position.coords.longitude, position.coords.latitude])
        //   .addTo(this.map);

        // this.map.setCenter([
        //   position.coords.longitude,
        //   position.coords.latitude
        // ]);

        if (markerLatitude && markerLongitude) {
          this.map.setCenter([
            markerLatitude,
            markerLongitude
          ]);
        } else {
          this.map.setCenter([
            position.coords.longitude,
            position.coords.latitude
          ]);
        }

        console.log(
          "📍 User's current position: " +
          "(" +
          position.coords.latitude +
          "," +
          position.coords.longitude +
          ")"
        );
      },
      error => {
        console.error("Geolocation error: ", error);

        // If error, direct the user to the White House
        this.map.setCenter([-77.0364976166554, 38.897684621644885]);
      }
    );

    this.map = new mapboxgl.Map({
      container: "map",
      style: "mapbox://styles/naivebara/clkyvh09v00m701me403i1svm",

      // White House
      center: [-77.0364976166554, 38.897684621644885],
      zoom: 12.5,
      minZoom: 4,
      maxZoom: 18
    });

    this.map.on("load", () => {
      this.addStores();
      // this.addDistricts();
    });
  },

  methods: {
    // Stores
    addStores() {
      fetch("/stores.json")
        .then(response => response.json())
        .then(data => {
          this.map.addSource("stores", {
            type: "geojson",
            data: data
          });

          // Define the source
          this.storeData = data;

          // Extract the data from json
          data.features.forEach(feature => {
            ["mini", "default", "larger", "active"].forEach(size => {
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

          // Setup the text of the stores' marker
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

          // Render the stores' marker as a layer
          this.map.addLayer({
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

              // Import higher resolution and compress to normal size
              "icon-size": 0.25,

              "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
              "text-field": ["step", ["zoom"], "", 13.5, ["get", "title"]],
              "text-anchor": "left"
            },
            paint: {
              "text-color": "#FFFFFF"
            }
          });

          // Pass the data to clickMarker
          this.map.on("click", "stores", event => this.clickMarker(event));

          // If click the map, reset the active stores' marker
          this.map.on("click", event => {
            // Check if the click event occurred on the stores layer
            const features = this.map.queryRenderedFeatures(event.point, {
              // assuming "stores" is the layer id where markers are
              layers: ["stores"]
            });

            // If the click event did not occur on the stores layer, remove the temporary marker
            if (!features.length && this.tempMarker) {
              this.tempMarker.remove();
              this.tempMarker = null;
            }
          });
        });
    },

    // Create a temp marker and move the center when click it
    clickMarker(event) {
      if (this.tempMarker) {
        this.tempMarker.remove();
      }

      const title = event.features[0].properties.title;
      /** 
       * When the event pass to clickMarker(), the Mapbox makes a new "features" that packages the data of the event
       * which means this "features" is a new features instead of the stores.json
       */
      const coordinates = event.features[0].geometry.coordinates;
      const iconString = event.features[0].properties.icon;
      const iconObject = JSON.parse(iconString);
      const activeIcon = iconObject.active;

      const router = useRouter();

      this.selectedStore = this.storeData.features.find(
        store => store.properties.title === title
      ).properties;

      // Create a temporary marker
      const el = document.createElement("div");
      el.className = "marker-active";
      el.style.backgroundImage = `url(${activeIcon})`;
      el.style.backgroundPosition = "center";
      el.style.backgroundRepeat = "no-repeat";
      el.style.backgroundSize = "contain";
      el.style.width = "52px";
      el.style.height = "79px";

      // // 🐞 Debug console
      // console.log("Icon: ", activeIcon);

      this.tempMarker = new mapboxgl.Marker(el, { offset: [0, -24] })
        .setLngLat(coordinates)
        .addTo(this.map);

      this.map.flyTo({
        center: [coordinates[0], coordinates[1]],
        offset: [0, -200],
        duration: 500,
        curve: 1
      });

      // Store latitude and longitude in local storage
      localStorage.setItem('markerLatitude', coordinates[0]);
      localStorage.setItem('markerLongitude', coordinates[1]);

      // // 🐞 Debug console
      // console.log("⬇️ Clicked the Marker");
      // console.log("title: " + title);
      // console.log("Selected Store:", this.selectedStore);
      // console.log("center: " + coordinates[0] + ", " + coordinates[1]);
    },

    // // District
    // addDistricts() {
    //   fetch("/districts.json")
    //     .then(response => response.json())
    //     .then(data => {
    //       this.map.addSource("districts", {
    //         type: "geojson",
    //         data: data
    //       });
    //       this.districtData = data;

    //       // Render the district's area
    //       this.map.addLayer({
    //         id: "districts",
    //         type: "fill",
    //         source: "districts",
    //         layout: {},
    //         paint: {
    //           "fill-color": "#3DC363",
    //           "fill-opacity": 0.6
    //         },
    //         filter: ["==", "$type", "Polygon"]
    //       });
    //       // Render the district's border
    //       this.map.addLayer({
    //         id: "outline",
    //         type: "line",
    //         source: "districts",
    //         layout: {},
    //         paint: {
    //           "line-color": "#3DC363",
    //           "line-width": 1
    //         },
    //         filter: ["==", "$type", "Polygon"]
    //       });

    //       // ↓ Extract the data from json
    //       // Load images
    //       data.features.forEach(feature => {
    //         if (feature.geometry.type === "Point") {
    //           ["mini", "default", "larger", "active"].forEach(size => {
    //             const iconPath =
    //               "/Button/Marker/" +
    //               feature.properties.type +
    //               "_" +
    //               size +
    //               ".png";
    //             this.map.loadImage(iconPath, (error, image) => {
    //               if (error) throw error;
    //               const iconName = feature.properties.type + "-" + size;
    //               this.map.addImage(iconName, image);
    //             });
    //           });
    //         }
    //       });

    //       // ↓ Setup the text of the districts' marker
    //       this.map.on("zoom", () => {
    //         const zoomLevel = this.map.getZoom();

    //         if (zoomLevel >= 14.5) {
    //           this.map.setLayoutProperty("markers", "text-offset", [1, 0]);
    //         } else if (zoomLevel >= 12.4) {
    //           this.map.setLayoutProperty("markers", "text-offset", [0.8, 0]);
    //         } else {
    //           this.map.setLayoutProperty("markers", "text-offset", [0, 0]);
    //         }
    //       });

    //       // Render the districts' marker as a layer
    //       this.map.addLayer({
    //         id: "markers",
    //         type: "symbol",
    //         source: "districts",
    //         layout: {
    //           "icon-image": [
    //             "step",
    //             ["zoom"],
    //             "", // this will display nothing from zoom levels 3-10
    //             10,
    //             ["concat", ["get", "type"], "-mini"],
    //             12.4,
    //             ["concat", ["get", "type"], "-default"],
    //             14.5,
    //             ["concat", ["get", "type"], "-larger"]
    //           ],
    //           "icon-size": 0.25,
    //           "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
    //           "text-field": ["step", ["zoom"], "", 13.5, ["get", "title"]],
    //           "text-anchor": "left"
    //         },
    //         paint: {
    //           "text-color": "#FFFFFF"
    //         },
    //         filter: ["==", "$type", "Point"]
    //       });
    //     });
    // },

    // Locate
    locateUser() {
      navigator.geolocation.getCurrentPosition(
        position => {
          this.map.flyTo({
            center: [position.coords.longitude, position.coords.latitude],
            zoom: 12.5, // optional zoom level
            speed: 2, // make the flying slow
            curve: 1 // change the speed at which it zooms out
          });
          console.log(
            "Locate the user to current position: "
            + "(" + position.coords.latitude + "," + position.coords.longitude + ")"
          );
        },
        error => {
          console.error("Geolocation error: ", error);
          // White House as default location
          this.map.setCenter([-77.0364976166554, 38.897684621644885]);
        }
      );
    },

    resetSelectedStore() {
      this.selectedStore = null;
      this.tempMarker.remove();
    }
  }
};
</script>

<style lang="scss" scoped>
#map {
  /* Prevent any unexpected overflow */
  overflow: hidden;

  position: relative;
  flex-direction: column;
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
