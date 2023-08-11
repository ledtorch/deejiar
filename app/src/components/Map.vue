<template>
  <div id="map"></div>
</template>

<script>
import mapboxgl from "mapbox-gl";

export default {
  data() {
    return {
      map: null,
    };
  },

  // ↓ Mount Mapbox
  mounted() {
    mapboxgl.accessToken =
      "pk.eyJ1IjoibmFpdmViYXJhIiwiYSI6ImNsa3lzZmV6ZzA1NHMzbW13ZjJ4aTJodzIifQ.kaC5YvO-g5idBZK4bDvZ7g";

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
            ["mini", "default", "larger"].forEach((size) => {
              const iconPath = "/" + feature.properties.icon[size];
              this.map.loadImage(iconPath, (error, image) => {
                if (error) throw error;
                this.map.addImage(feature.properties.title + "-" + size, image);
                if (size === "mini") {
                  console.log("Mini image loaded:", iconPath);
                }
              });
            });
          });

          this.map.on("zoom", () => {
            const zoomLevel = this.map.getZoom();

            if (zoomLevel >= 14.5) {
              this.map.setLayoutProperty("points", "text-offset", [1, 0]);
            } else if (zoomLevel >= 12.5) {
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
            console.log("Click!");
            const title = e.features[0].properties.title;
            this.$router.push({
              name: "store",
              params: { title: encodeURIComponent(title) },
            }); // Encode the title
          });
        });
    },
  },
};
</script>

<style>
#map {
  width: 100vw;
  height: 100vh;
}
</style>
