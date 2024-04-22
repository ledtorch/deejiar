<template>
  <div class="frame">
    <div class="icon"></div>
    <p class="subhead">{{ address }}</p>
  </div>
</template>

<script>
export default {
  props: {
    address: String
  }
};
</script>

<style lang="scss" scoped>
/* .review-frame {
} */

.frame {
  align-items: flex-start;
  gap: 8px;
  align-self: stretch;
}

.icon {
  min-width: 24px;
  height: 24px;
  background: url("/icon/info/address.png") no-repeat center/contain;
}
</style>
