<template>
  <div class="bottom-sheet">
    <h1>{{ store.properties.title }}</h1>
    <p>{{ store.properties.description }}</p>
    <p>This is ME</p>
    <!-- Display other store information as needed -->
  </div>
</template>

<script>
export default {
  props: ["store"],

  mounted() {
    console.log("Store:", this.store);
  },
};
</script>

<style>
.bottom-sheet {
  position: absolute;
  z-index: 1;
  width: 100%;
  height: 76px;
  bottom: 0;
  padding: 12px 16px 16px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  border-radius: 12px 12px 0px 0px;
  background-color: #ffffff;
  /* Add additional styling as needed */
}
</style>
