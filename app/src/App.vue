<script setup>
import "mapbox-gl/dist/mapbox-gl.css";
// Mapbox Dependency

import { useRouter } from "vue-router";
const router = useRouter();
</script>

<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<style scoped>
</style>
