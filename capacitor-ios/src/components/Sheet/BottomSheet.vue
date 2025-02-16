<template>
  <div class="bottom-sheet flex-col" :style="{ height: bottomSheetHeight }" ref="bottomSheet">
    <div class="control-area" ref="controlArea">
      <div class="control-bar"></div>
    </div>

    <!-- v-show for static content -->
    <div class="bottom-sheet-content" v-show="!storeState">
      <Avatar />
      <h4>Wanna get the premium list and advanced features before they launch on Deejiar? Or simply want to leave your
        feedback? =)</h4>
      <a href="https://www.buymeacoffee.com/deejiar" alt="Buy Me a Coffee" class="buy-me-a-coffee-button">
        <img
          src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=deejiar&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff"
          alt="Buy Me a Coffee" />
      </a>
      <div class="frame_learn-more">
        <h4>Learn more on:</h4>
        <div class="button-set">
          <a href="https://twitter.com/deejiar" style="text-decoration: none; color: inherit;">
            <div>
              <img class="social-button" src="/icon/social/twitter.png" alt="Twitter">
              <p>@deejiar</p>
            </div>
          </a>
          <a href="https://www.instagram.com/deejiar" style="text-decoration: none; color: inherit;">
            <div>
              <img class="social-button" src="/icon/social/instagram.png" alt="Instagram">
              <p>@deejiar</p>
            </div>
          </a>
        </div>
      </div>
    </div>

    <div class="bottom-sheet-content" v-if="storeState">
      <!-- Template Food -->
      <template v-if="storeLayout === 'food'">
        <div class="nav">
          <div class="title-block">
            <h2 class="_stretch">{{ store ? store.title : "" }}</h2>
            <TagShopType :store="store" />
          </div>
          <Close :state="buttonState" @close="closeBottomSheet" />
        </div>
        <div class="image-div">
          <div class="main-column" :style="{ 'backgroundImage': storeImages.storefront }"></div>
          <div class="secondary-column">
            <div class="image" :style="{ 'backgroundImage': storeImages.item1 }"></div>
            <div class="image" :style="{ 'backgroundImage': storeImages.item2 }"></div>
          </div>
        </div>
        <div class="state">
          <p class="text-limited">{{ store ? store.description : "" }}</p>
        </div>
        <!-- <Review /> -->
        <Businesshour :bizTime="store.businesshour" viewMode="overview" />
        <div class="key-info-div"></div>
      </template>

      <!-- Template View -->
      <template v-if="storeLayout === 'view'">
        <div class="nav">
          <div class="title-block">
            <h2 class="_stretch">{{ store ? store.title : "" }}</h2>
            <TagShopType :store="store" />
          </div>
          <Close :state="buttonState" @close="closeBottomSheet" />
        </div>
        <div class="image-div">
          <div class="main-column--view" :style="{ 'backgroundImage': storeImages.storefront }"></div>
        </div>
        <div class="state">
          <p class="text-limited">{{ store ? store.description : "" }}</p>
        </div>
        <Businesshour :bizTime="store.businesshour" viewMode="overview" />
        <div class="key-info-div"></div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, defineAsyncComponent } from 'vue';
import { useRouter } from 'vue-router';

// Button
const Avatar = defineAsyncComponent(() => import("./Avatar.vue"));
const TagShopType = defineAsyncComponent(() => import("../Button/TagShopType.vue"));
const Close = defineAsyncComponent(() => import("../Button/Icon/Close.vue"));

// Components
const Businesshour = defineAsyncComponent(() => import("./Businesshour.vue"));
// const Review = defineAsyncComponent(() => import("./Review.vue"));

// Props
const props = defineProps({
  store: Object
});

// Constants
const minHeight = "32px";
const maxHeight = "100%";
const withStoreHeight = "467px";
const deviceHeight = `calc(100vh - env(safe-area-inset-top))`

// Refs
const isDragging = ref(false);
const bottomSheetHeight = ref("32px");
const bottomSheet = ref(null);
const controlArea = ref(null);
const buttonState = ref("default");

// Render store properties
const rootUrl = (imagePath) => {
  const baseUrl = `${window.location.protocol}//${window.location.host}`;
  return `url('${baseUrl}/${imagePath}')`;
};

const storeState = computed(() => props.store);
const storeLayout = computed(() => props.store?.layout);
const storeImages = computed(() => ({
  storefront: rootUrl(props.store.storefront.day),
  item1: rootUrl(props.store.item1.image),
  item2: rootUrl(props.store.item2.image)
}));


// Expand BottomSheet when user clicks store marker
watch(() => props.store, (newStore) => {
  if (newStore !== null) {
    bottomSheetHeight.value = withStoreHeight;
    // // 🐞 Debug console
    // console.log("json: " + JSON.stringify(props.store, null, 2));
    // console.log("layout: " + props.store?.layout);
    // console.log("storefront image URL: " + rootUrl(props.store?.storefront.day));
    // console.log("item1 image URL: " + rootUrl(props.store?.item1?.image));
    // console.log("item2 image URL: " + rootUrl(props.store?.item2?.image));
  }
});

// Dragging logic
const router = useRouter();
let startY = 0;
let startHeight = 0;

const updateSheetHeight = (height) => {
  bottomSheetHeight.value = `${height}`;
};

const dragStart = (event) => {
  // // 🐞 Debug console
  // console.log("dragStart");

  // Assign startY to pageY(mouse / touch screen)
  isDragging.value = true;
  startY = event.pageY || event.touches?.[0].pageY;
  startHeight = parseInt(bottomSheetHeight.value);
  bottomSheet.value.classList.add("dragging");
  // // 🐞 Debug console
  // console.log("startHeight: " + startHeight + " & " + "startY: " + startY);

  // Add listener
  document.addEventListener("mousemove", dragging);
  document.addEventListener("mouseup", dragStop);
  document.addEventListener("touchmove", dragging);
  document.addEventListener("touchend", dragStop);
};

const dragStop = () => {
  // // 🐞 Debug console
  // console.log("dragStop");

  isDragging.value = false;
  bottomSheet.value.classList.remove("dragging");
  const sheetHeight = parseInt(bottomSheet.value.style.height);

  // Navigate to detail.vue
  if (sheetHeight >= 600 && props.store?.title) {
    router.push({
      name: "detail",
      params: {
        title: props.store.title,
      }
    });
  } else if (sheetHeight >= 600 && !props.store?.title) {
    console.log("deviceHeight: " + deviceHeight);
    updateSheetHeight(deviceHeight);
  } else if (sheetHeight < 150) {
    updateSheetHeight(minHeight);
  } else if (sheetHeight > 500) {
    updateSheetHeight(maxHeight);
  } else {
    updateSheetHeight(withStoreHeight);
  }

  // Remove listener
  document.removeEventListener("mousemove", dragging);
  document.removeEventListener("touchmove", dragging);
  document.removeEventListener("mouseup", dragStop);
  document.removeEventListener("touchend", dragStop);
};

const dragging = (event) => {
  // // 🐞 Debug console
  // console.log("Dragging");

  if (!isDragging.value) return;
  const delta = startY - (event.pageY || event.touches?.[0].pageY);
  const newHeight = startHeight + delta;
  updateSheetHeight(newHeight + "px");
  // // 🐞 Debug console
  // console.log("newHeight: " + newHeight + " & " + "delta: " + delta);
};

// Close BottomSheet
const emit = defineEmits(['reset']);
const closeBottomSheet = () => {
  emit("reset");
};

// Lifecycle hooks
onMounted(() => {
  controlArea.value.addEventListener("mousedown", dragStart);
  controlArea.value.addEventListener("touchstart", dragStart);
});
</script>

<style lang="scss" scoped>
.bottom-sheet {
  gap: 0px;
  width: 100%;
  height: 100%;
  min-height: 32px;
  max-height: 100%;
  padding: 0px 16px 16px 16px;
  border-radius: 12px 12px 0px 0px;
  background-color: #000;
  transition: height 0.3s ease;
}

.bottom-sheet-content {
  flex-direction: column;
  gap: 12px;
  background-color: #000;
}

.control-area {
  cursor: grab;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  align-self: stretch;
  height: 32px;
  padding: 16px 0px 12px 0px;
}

.control-area:active {
  cursor: grabbing;
}

.control-bar {
  cursor: grab;
  flex-shrink: 0;
  width: 48px;
  height: 4px;
  border-radius: 4px;
  background-color: #808cab;
}

.nav {
  gap: 12px;
}

.title-block {
  justify-content: flex-start;
  align-content: flex-start;
  align-self: stretch;
  flex-wrap: wrap;
  flex: 1 0 0;
  gap: 12px;
}

.image-div {
  align-items: flex-end;
  align-self: stretch;
  gap: 8px;
}

.main-column {
  width: 180px;
  height: 180px;
  border-radius: 12px;

  // Image setting
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.main-column--view {
  width: 100%;
  height: 260px;
  border-radius: 12px;

  // Image setting
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.button-set {
  align-items: flex-start;
  align-self: stretch;
  gap: 12px;
}

.social-button {
  width: 24px;
  height: 24px;
}

.image {
  align-self: stretch;
  height: 86px;
  border-radius: 12px;

  // Image setting
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.secondary-column {
  flex-direction: column;
  justify-content: flex-end;
  align-items: flex-start;
  flex: 1 0 0;
  gap: 8px;
}

.state {
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  padding: 12px;
  border-radius: var(--border-button-round, 8px);
  background: var(--4-base-dark-base, rgba(255, 255, 255, 0.07));
}

.text-limited {
  max-height: 48px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  /* Adjust to the number of lines you want to display */
  -webkit-box-orient: vertical;
  text-overflow: ellipsis;
}

.key-info-div {
  flex-direction: column;
  align-self: stretch;
  gap: 12px;
}

.businesshour-frame {
  gap: 4px;
}

.frame_learn-more {
  flex-direction: column;
  gap: 12px;
  align-self: stretch;
}

.buy-me-a-coffee-button img {
  width: 235px;
  height: 50px;
  display: block;
}
</style>