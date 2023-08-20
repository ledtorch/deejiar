<template>
  <div
    class="bottom-sheet"
    :style="{ height: bottomSheetHeight }"
    ref="bottomSheet"
  >
    <div class="control-area" ref="controlArea">
      <div class="control-bar"></div>
    </div>

    <div class="bottom-sheet-content" v-if="!storeState">
      <Avatar />
    </div>

    <div class="bottom-sheet-content" v-if="storeState">
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
        <div class="state">{{ store ? store.description : "" }}</div>
        <Review />
        <Businesshour :store="store" />
        <div class="key-info-div"></div>
      </template>
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
        <div class="state">{{ store ? store.description : "" }}</div>
        <Review />
        <Businesshour :store="store" />
        <div class="key-info-div"></div>
      </template>
    </div>
  </div>
</template>


<script>
import { ref, onMounted, watch, toRefs, computed } from "vue";

import IconButtonClose from "../Button/IconButtonClose.vue";
import TagShopType from "../Button/TagShopType.vue";
import Avatar from "./Avatar.vue";
import Review from "./Review.vue";
import Businesshour from "./Businesshour.vue";
import { useRouter } from "vue-router";

export default {
  components: { IconButtonClose, TagShopType, Avatar, Review, Businesshour },
  data() {
    return {
      buttonState: "default",
    };
  },
  name: "BottomSheet",
  props: {
    store: Object,
  },

  setup(props) {
    const router = useRouter();

    const isDragging = ref(false);
    const bottomSheetHeight = ref("32px");
    const bottomSheet = ref(null);
    const controlArea = ref(null);
    // Use ref to bound to DOM

    let startY = 0;
    let startHeight = 0;
    const minHeight = `32px`;
    const withStoreHeight = `467px`;
    const maxHeight = `100%`;
    // Initialize values for dragging fn'

    const { store } = toRefs(props); // Convert props to reactive references

    const isContent = computed(
      () => store.value !== null && store.value !== undefined
    );

    // Watch the store value for changes
    watch(store, (newStore, oldStore) => {
      if (newStore !== null) {
        bottomSheetHeight.value = withStoreHeight;
      }
    });

    const updateSheetHeight = (height) => {
      bottomSheetHeight.value = `${height}`;
      console.log("👉 updateSheetHeight: " + bottomSheetHeight.value);
      // Toggles the fullscreen class to bottomSheet if the height is equal to 100
      // bottomSheet.classList.toggle("fullscreen", height === 100);
    };

    const dragStart = (event) => {
      console.log("dragStart");

      isDragging.value = true;
      startY = event.pageY || event.touches?.[0].pageY;
      // Assign startY to pageY(mouse) or pageY(touch screen)

      startHeight = parseInt(bottomSheetHeight.value);
      bottomSheet.value.classList.add("dragging");
      console.log("startHeight: " + startHeight + " & " + "startY: " + startY);
      console.log(
        "bottomSheet.value.classList: " + bottomSheet.value.classList
      );

      document.addEventListener("mousemove", dragging);
      document.addEventListener("mouseup", dragStop);
      document.addEventListener("touchmove", dragging);
      document.addEventListener("touchend", dragStop);
      // Add listener
    };

    const dragStop = () => {
      console.log("dragStop");
      isDragging.value = false;
      bottomSheet.value.classList.remove("dragging");
      const sheetHeight = parseInt(bottomSheet.value.style.height);
      sheetHeight < 150
        ? updateSheetHeight(minHeight)
        : sheetHeight > 500
        ? updateSheetHeight(maxHeight)
        : updateSheetHeight(withStoreHeight);

      document.removeEventListener("mousemove", dragging);
      document.removeEventListener("touchmove", dragging);
      document.removeEventListener("mouseup", dragStop);
      document.removeEventListener("touchend", dragStop);
      // Remove listener
    };

    const dragging = (event) => {
      console.log("Dragging");

      if (!isDragging.value) return;
      const delta = startY - (event.pageY || event.touches?.[0].pageY);
      const newHeight = startHeight + delta;

      updateSheetHeight(newHeight + `px`);

      console.log("newHeight: " + newHeight + " & " + "delta: " + delta);
    };

    onMounted(() => {
      controlArea.value.addEventListener("mousedown", dragStart);
      controlArea.value.addEventListener("touchstart", dragStart);
    });
    return {
      controlArea,
      bottomSheet,
      bottomSheetHeight,
    };
  },

  methods: {
    closeBottomSheet() {
      this.$emit("reset");
    },
  },

  computed: {
    storeState() {
      return this.store;
    },

    // storeState() {
    //   if (this.store === true) {
    //     return this.store;
    //   }
    // },

    storeLayout() {
      console.log("Compute storeLayout:" + this.store?.layout); // ← 🐞 Debug console
      return this.store?.layout;
    },

    mainColumnImage() {
      // console.log("📃 Storefront URL: " + this.store?.storefront); // ← 🐞 Debug console
      return `background: url('${this.store?.storefront}') center/cover no-repeat;`;
    },
    item1() {
      // console.log("📃 item1 URL: " + this.store?.item1); // ← 🐞 Debug console
      return `background: url('${this.store?.item1}') center/cover no-repeat;  `;
    },
    item2() {
      // console.log("📃 item2 URL: " + this.store?.item2); // ← 🐞 Debug console
      return `background: url('${this.store?.item2}') center/cover no-repeat;`;
    },
  },
};
</script>


<style scoped>
.bottom-sheet {
  width: 390px;
  min-height: 32px;
  max-height: 100%;
  /* Define the min and max of the BottomSheet comp */
  height: auto;
  padding: 0px 16px 16px 16px;
  border-radius: 12px 12px 0px 0px;
  flex-direction: column;
  gap: 0px;
  background-color: #000;
  transition: height 0.3s ease;
}

.bottom-sheet-content {
  flex-direction: column;
  gap: 12px;
}

.control-area {
  height: 32px;
  padding: 16px 0px 12px 0px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  align-self: stretch;
  cursor: grab;
}

.control-area:active {
  cursor: grabbing;
}

.control-bar {
  cursor: grab;
  width: 48px;
  height: 4px;
  flex-shrink: 0;
  border-radius: 4px;
  background-color: #808cab;
}

.nav {
  /* align-items: flex-start; */
  /* height: auto; */
  gap: 12px;
  /* align-self: stretch; */
}

.title-block {
  align-items: flex-start;
  justify-content: flex-start;
  align-content: flex-start;
  gap: 12px;
  flex: 1 0 0;
  align-self: stretch;
  flex-wrap: wrap;
}

.image-div {
  align-items: flex-end;
  gap: 8px;
  align-self: stretch;
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
  border-radius: 12px;
  height: 86px;
  align-self: stretch;
  background-size: cover;
  background-repeat: no-repeat;
}

.secondary-column {
  flex-direction: column;
  justify-content: flex-end;
  align-items: flex-start;
  gap: 8px;
  flex: 1 0 0;
}

.state {
  padding: 12px;
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  border-radius: var(--border-button-round, 8px);
  background: var(--4-base-dark-base, rgba(255, 255, 255, 0.07));
}

.key-info-div {
  flex-direction: column;
  align-items: flex-start;
  gap: 12px;
  align-self: stretch;
}

.stretch {
  flex: 1 0 0;
}

.businesshour-frame {
  gap: 4px;
}
</style>