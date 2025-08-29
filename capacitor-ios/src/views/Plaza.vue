<template>
  <main class="body">
  </main>
</template>

<script setup>
</script>

<style lang="scss" scoped>
.body {
  display: flex;
  position: relative;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  overflow-y: auto;

  /* Media query for screen widths 430px and below */
  @media (max-width: 430px) {
    padding-bottom: 99px;
  }
}
</style>