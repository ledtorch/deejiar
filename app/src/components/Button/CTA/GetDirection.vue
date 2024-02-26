<template>
  <button @click="openDirections" class="btton-frame">
    <div class="title-frame">
      <div class="apple-maps"></div>
      <h2 class="m-button-text">Get Direction</h2>
    </div>
    <div class="outer-link"></div>
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

/* Reset button styles */
button,
input[type="button"],
input[type="reset"],
input[type="submit"] {
  background: none;
  color: inherit;
  /* Use the text color of the element the button is inside */
  border: none;
  padding: 0;
  font: inherit;
  /* Use the font settings of the element the button is inside */
  cursor: pointer;
  outline: inherit;
  /* Use the outline settings of the element the button is inside */
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
  background: url("/Button/Icon/brand/appleMaps.svg") no-repeat center/contain;
}

.outer-link {
  width: 24px;
  height: 24px;
  background: url("/Button/Icon/controlData/outerLink.svg") no-repeat center/contain;
}
</style>
