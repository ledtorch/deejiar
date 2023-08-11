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
};
</script>

<style>
.bottom-sheet {
  /* Add styles to position the bottom sheet at the bottom of the screen and make it look like a bottom sheet */
  /* width: 100px;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #ffffff; */
  /* Add additional styling as needed */
}
</style>
