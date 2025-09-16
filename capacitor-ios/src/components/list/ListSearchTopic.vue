<template>
  <button class="list-container">
    <div class="topic-header">

      <img src="@/assets/images/taipei.jpg" alt="Taipei" class="topic-icon">
      <p class="topic-title _title">Start from Taipei City</p>
    </div>

    <img src="@/assets/button/pin-point.svg" alt="Pin location" class="topic-button-icon" />
  </button>
</template>

<script setup>

</script>

<style lang="scss" scoped>
.list-container {
  display: flex;
  width: 100%;
  padding: var(--atom);
  justify-content: space-between;
  align-items: center;
  border-radius: var(--round-m);
  background-color: var(--gray-button);

  &:active {
    opacity: 0.7;
  }
}

.topic-header {
  align-items: center;
  gap: var(--unit);
}

.topic-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--round-s);
}

.topic-button-icon {
  width: 24px;
  height: 24px;
}

.topic-title {
  color: var(--primary-text);
}
</style>