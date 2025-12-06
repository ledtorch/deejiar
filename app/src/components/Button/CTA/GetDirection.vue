<template>
  <button @click="openDirections" class="button-frame">
    <div class="title-frame">
      <div :class="iconClass"></div>
      <p class="_button-secondary">Get Direction</p>
    </div>
    <div class="outer-link icon-themed"></div>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    required: true,
  },
  storeTitle: String,

  appleAUID: String,
  // 🏗️ TODO
  googlePlaceid: String,
})

// computed: iconClass
const iconClass = computed(() => {
  return props.variant === 'apple' ? 'apple-maps' : 'google-maps'
})

// computed: directionUrl
const directionUrl = computed(() => {
  if (props.variant === 'apple') {
    // 🐞 Debug console
    console.log('appleAUID:', props.appleAUID)
    /** 
     * https://developer.apple.com/library/archive/featuredarticles/iPhoneURLScheme_Reference/MapLinks/MapLinks.html
     * e.g. &dirflg=d is travel by car
     */
    return `https://maps.apple.com/?auid=${props.appleAUID}&dirflg=d`
  } else if (props.variant === 'google') {
    // 🏗️ TODO
    // 🐞 Debug console
    // console.log('googlePlaceID:', props.googlePlaceid)
    // console.log('v1:', `https://www.google.com/maps/dir/?api=1&destination=place_id:${props.googlePlaceid}&travelmode=flying`)
    // console.log('v2:', `https://www.google.com/maps/dir/?api=1&destination=place_id:${props.googlePlaceid}`)
    // https://www.google.com/maps/dir/?api=1&destination_place_id=ChIJwSO8jsCrQjQRqDmCOu8hCbA
    // https://www.google.com/maps/dir/?api=1&origin=Taipei+101+Shopping+center&destination_place_id=ChIJwSO8jsCrQjQRqDmCOu8hCbA
    // console.log('place only:', `https://www.google.com/maps/place/?q=place_id:${props.googlePlaceid}`)
    // console.log('place with encodeURI:', `https://www.google.com/maps/place/?q=place_id:${encodeURIComponent(props.googlePlaceid)}`)
    // console.log('id+geo:', `https://www.google.com/maps/search/?api=1&query=${props.geoData}&query_place_id=${props.googlePlaceid}`)

    /** 
     * https://developers.google.com/maps/documentation/urls/get-started
     * If the title is Mandarin, convert the data before (
     * If the title is English, convert the blank to '+'' symbol
     */
    const title = encodeURIComponent(
      props.storeTitle.split('(')[0].trim()
    ).replace(/%20/g, '+')

    // Default travel mode is flying but Google Maps will convert to driving if it's not international
    return `https://www.google.com/maps/dir/?api=1&destination=${title}&travelmode=flying`

    // 🏗️ TODO
    // return `https://www.google.com/maps/dir/?api=1&destination=destination_place_id:${props.googlePlaceid}&travelmode=flying`;
    // return `https://www.google.com/maps/place/?q=place_id:${encodeURIComponent(props.googlePlaceid)}`;
    // return `https://www.google.com/maps/place/?q=place_id:${props.googlePlaceid}`;
    // https://www.google.com/maps/place/?q=place_id:ChIJwSO8jsCrQjQRqDmCOu8hCbA
  }
})

// method → normal function
function openDirections() {
  console.log('Opening URL:', directionUrl.value)
  window.open(directionUrl.value)
}
</script>

<style lang="scss" scoped>
.button-frame {
  display: flex;
  height: 48px;
  width: 100%;
  padding: 12px;
  justify-content: space-between;
  align-items: center;
  border-radius: var(--Border-Button-Round, 8px);
  background: var(--content);
}

/* Reset button styles */
button,
input[type="button"],
input[type="reset"],
input[type="submit"] {
  background: none;
  color: inherit;
  /* Use the text color of the element the button is inside */
  font: inherit;
  /* Use the font settings of the element the button is inside */
  cursor: pointer;
  outline: inherit;
  /* Use the outline settings of the element the button is inside */
}

.title-frame {
  align-items: center;
  gap: 4px;
}

.apple-maps {
  width: 24px;
  height: 24px;
  background: url("/button/icon/brand/apple-maps.png") no-repeat center/contain;
}

.google-maps {
  width: 24px;
  height: 24px;
  background: url("/button/icon/brand/google-maps.png") no-repeat center/contain;
}

.outer-link {
  width: 24px;
  height: 24px;
  background: url("/button/icon/control-data/outer-link.svg") no-repeat center/contain;
}
</style>
