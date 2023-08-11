<script setup>
import "mapbox-gl/dist/mapbox-gl.css";
// Mapbox Dependency

import Map from "./components/Map.vue";
import BottomSheet from "./components/BottomSheet.vue";

import { useRouter } from "vue-router";
const router = useRouter();
</script>

<template>
  <div>
    <router-view></router-view>
    <Map />
    <BottomSheet />
  </div>
</template>

<style scoped>
</style>
