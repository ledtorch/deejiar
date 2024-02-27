<template>
  <button @click="openDirections" class="btton-frame">
    <div class="title-frame">
      <div :class="iconClass"></div>
      <h2 class="m-button-text">Get Direction</h2>
    </div>
    <div class="outer-link"></div>
  </button>
</template>

<script>
export default {
  props: {
    variant: {
      type: String,
      required: true,
    },
    appleAUID: String,
    storeTitle: String,
  },
  computed: {
    iconClass() {
      return this.variant === 'apple' ? 'apple-maps' : 'google-maps';
    },
    directionUrl() {
      if (this.variant === 'apple') {
        // 🐞 Debug console
        console.log('appleAUID:', this.appleAUID)
        /** 
         * https://developer.apple.com/library/archive/featuredarticles/iPhoneURLScheme_Reference/MapLinks/MapLinks.html
         * e.g. &dirflg=d is travel by car
         */
        return `https://maps.apple.com/?auid=${this.appleAUID}&dirflg=d`;
      } else if (this.variant === 'google') {
        // 🐞 Debug console
        console.log('storeTitle:', this.storeTitle)
        /** 
         * If the title is Mandarin, convert the data before (
         * If the title is English, convert the blank to '+'' symbol
         */
        const title = encodeURIComponent(this.storeTitle.split('(')[0].trim()).replace(/%20/g, '+');

        // Default travel mode is flying but Google Maps will convert to driving if it's not international
        return `https://www.google.com/maps/dir/?api=1&destination=${title}&travelmode=flying`;
      }
    },
  },
  methods: {
    openDirections() {
      window.open(this.directionUrl);
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
  background: url("/Button/Icon/brand/appleMaps.png") no-repeat center/contain;
}

.google-maps {
  width: 24px;
  height: 24px;
  background: url("/Button/Icon/brand/googleMaps.png") no-repeat center/contain;
}

.outer-link {
  width: 24px;
  height: 24px;
  background: url("/Button/Icon/controlData/outerLink.svg") no-repeat center/contain;
}
</style>
