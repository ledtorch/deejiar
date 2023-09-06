<template>
  <div class="bottom-sheet" :style="{ height: bottomSheetHeight }" ref="bottomSheet">
    <div class="control-area" ref="controlArea">
      <div class="control-bar"></div>
    </div>

    <div class="bottom-sheet-content" v-if="!storeState">
      <Avatar />
    </div>

    <div class="bottom-sheet-content" v-if="storeState">
      <!-- Template Food -->
      <template v-if="storeLayout === 'food'">
        <div class="nav">
          <div class="title-block">
            <h2 class="stretch">{{ store ? store.title : "" }}</h2>
            <TagShopType :store="store" />
          </div>
          <IconButtonClose :state="buttonState" @close="closeBottomSheet" />
        </div>
        <div class="image-div">
          <div class="main-column" :style="mainColumnImage"></div>
          <div class="secondary-column">
            <div class="image" :style="item1"></div>
            <div class="image" :style="item2"></div>
          </div>
        </div>
        <div class="state">
          <p class="text-limited">{{ store ? store.description : "" }}</p>
        </div>
        <Review />
        <Businesshour :bizTime="store.businesshour" viewMode="overview" />
        <div class="key-info-div"></div>
      </template>

      <!-- Template View -->
      <template v-if="storeLayout === 'view'">
        <div class="nav">
          <div class="title-block">
            <h2 class="stretch">{{ store ? store.title : "" }}</h2>
            <TagShopType :store="store" />
          </div>
          <IconButtonClose :state="buttonState" @close="closeBottomSheet" />
        </div>
        <div class="image-div">
          <div class="main-column--view" :style="mainColumnImage"></div>
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

<script>
// Vue Dependencies
import { ref, onMounted, watch, toRefs, computed } from "vue";
import { useRouter } from "vue-router";

// Components
import IconButtonClose from "../Button/IconButtonClose.vue";
import TagShopType from "../Button/TagShopType.vue";
import Avatar from "./Avatar.vue";
import Review from "./Review.vue";
import Businesshour from "./Businesshour.vue";

export default {
  components: { IconButtonClose, TagShopType, Avatar, Review, Businesshour },
  data() {
    return {
      buttonState: "default"
    };
  },
  name: "BottomSheet",
  props: {
    store: Object
  },

  setup(props) {
    const router = useRouter();

    // Use ref to bound to DOM
    const isDragging = ref(false);
    const bottomSheetHeight = ref("32px");
    const bottomSheet = ref(null);
    const controlArea = ref(null);

    // Initialize values for dragging fn'
    let startY = 0;
    let startHeight = 0;
    const minHeight = `32px`;
    const withStoreHeight = `467px`;
    const maxHeight = `100%`;

    // Convert props to reactive references
    const { store } = toRefs(props);

    // Watch the store value for changes
    watch(store, newStore => {
      if (newStore !== null) {
        bottomSheetHeight.value = withStoreHeight;
      }
    });

    const updateSheetHeight = height => {
      bottomSheetHeight.value = `${height}`;
    };

    const dragStart = event => {
      console.log("dragStart");

      // Assign startY to pageY(mouse) or pageY(touch screen)
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
      console.log("dragStop");
      isDragging.value = false;
      bottomSheet.value.classList.remove("dragging");
      const sheetHeight = parseInt(bottomSheet.value.style.height);

      // Navigate to detail.vue
      if (sheetHeight >= 600) {
        if (store && props.store.title) {
          router.push({
            name: "detail",
            params: {
              title: props.store.title,

              // Convert the obj into a string and pass it to router
              dataFromBottomSheet: JSON.stringify(props.store)
            }
          });
          console.log("dataFromBottomSheet:", this.dataFromBottomSheet);
        }
        sheetHeight < 150
          ? updateSheetHeight(minHeight)
          : sheetHeight > 500
            ? updateSheetHeight(maxHeight)
            : updateSheetHeight(withStoreHeight);
      }

      // Remove listener
      document.removeEventListener("mousemove", dragging);
      document.removeEventListener("touchmove", dragging);
      document.removeEventListener("mouseup", dragStop);
      document.removeEventListener("touchend", dragStop);
    };

    const dragging = event => {
      console.log("Dragging");

      if (!isDragging.value) return;
      const delta = startY - (event.pageY || event.touches?.[0].pageY);
      const newHeight = startHeight + delta;

      updateSheetHeight(newHeight + `px`);
      // // 🐞 Debug console
      // console.log("newHeight: " + newHeight + " & " + "delta: " + delta);
    };

    onMounted(() => {
      controlArea.value.addEventListener("mousedown", dragStart);
      controlArea.value.addEventListener("touchstart", dragStart);
    });
    return {
      controlArea,
      bottomSheet,
      bottomSheetHeight
    };
  },

  methods: {
    closeBottomSheet() {
      this.$emit("reset");
    }
  },

  computed: {
    storeState() {
      return this.store;
    },

    storeLayout() {
      // // 🐞 Debug console
      // console.log("Compute storeLayout: " + this.store?.layout);
      return this.store?.layout;
    },

    mainColumnImage() {
      // // 🐞 Debug console
      // console.log("📃 Storefront URL: " + this.store?.storefront);
      return `background: url('${this.store?.storefront}') center/cover no-repeat;`;
    },
    item1() {
      // // 🐞 Debug console
      // console.log("📃 item1 URL: " + this.store?.item1);
      return `background: url('${this.store?.item1.image}') center/cover no-repeat;  `;
    },
    item2() {
      // // 🐞 Debug console
      // console.log("📃 item2 URL: " + this.store?.item2);
      return `background: url('${this.store?.item2.image}') center/cover no-repeat;`;
    }
  }
};
</script>


<style lang="scss" scoped>
.bottom-sheet {
  flex-direction: column;
  gap: 0px;
  width: 390px;
  height: auto;
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
  align-items: flex-start;
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
}

.main-column--view {
  width: 100%;
  height: 260px;
  border-radius: 12px;
}

.image {
  align-self: stretch;
  height: 86px;
  border-radius: 12px;
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
  align-items: flex-start;
  align-self: stretch;
  gap: 12px;
}

.stretch {
  flex: 1 0 0;
}

.businesshour-frame {
  gap: 4px;
}
</style>