<template>
  <button @click="openDirections" class="btton-frame">
    <div class="title-frame">
      <div class="apple-maps"></div>
      <h2 class="m-button-text">Get Direction</h2>
    </div>
  </button>
</template>

<script>
export default {
  props: {
    geo: Array
  },
  methods: {
    openDirections() {
      console.log('geo:', this.geo)
      const [longitude, latitude] = this.geo;
      console.log('Geo data [lat, lon]:', [latitude, longitude])
      const url = `http://maps.apple.com/?daddr=${latitude},${longitude}&dirflg=d`;
      console.log('Apple Maps URL:', url)
      window.open(url, '_blank');
    }
  }
}
</script>

<style lang="scss" scoped>
.btton-frame {
  display: flex;
  height: 48px;
  width: 100%;
  padding: 12px;
  justify-content: space-between;
  align-items: center;
  flex: 1 0 0;
  border-radius: var(--Border-Button-Round, 8px);
  background: rgba(255, 255, 255, 0.07);
}

.title-frame {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4px;
}

.apple-maps {
  width: 24px;
  height: 24px;
  background: url("/Button/Icon/apple/maps.svg") no-repeat center/contain;
}

.outer-link {
  width: 24px;
  height: 24px;
  background: url("/Button/Icon/controlData/outerLink.svg") no-repeat center/contain;
}
</style>
