<template>
  <div
    class="bottom-sheet"
    :style="{ height: bottomSheetHeight }"
    ref="bottomSheet"
  >
    <div class="control-area" ref="controlArea">
      <div class="control-bar"></div>
    </div>
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
    <div class="key-info-div"></div>
  </div>
</template>


<script>
import { ref, onMounted } from "vue";

import IconButtonClose from "./Button/IconButtonClose.vue";
import TagShopType from "./Button/TagShopType.vue";
import Avatar from "./Avatar.vue";
import { useRouter } from "vue-router";

export default {
  components: { IconButtonClose, TagShopType, Avatar },
  data() {
    return {
      buttonState: "default",
    };
  },
  name: "BottomSheet",
  props: {
    store: Object,
  },

  setup() {
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
      this.bottomSheetHeight = "32px";
    },
  },

  computed: {
    showAvatar() {
      return !this.store;
    },

    mainColumnImage() {
      console.log("📃 Storefront URL: " + this.store?.storefront);
      console.log("📃 item1 URL: " + this.store?.item1);
      console.log("📃 item2 URL: " + this.store?.item2);
      return `background: url('${this.store?.storefront}') center/cover no-repeat;`;
    },
    item1() {
      return `background: url('${this.store?.item1}') center/cover no-repeat;  `;
    },
    item2() {
      return `background: url('${this.store?.item2}') center/cover no-repeat;`;
    },
    // Store data
  },
};
</script>


<style scoped>
.bottom-sheet {
  display: flex;
  width: 390px;
  min-height: 32px;
  max-height: 100%;
  /* Define the min and max of the BottomSheet comp */
  height: auto;
  padding: 0px 16px 16px 16px;
  border-radius: 12px 12px 0px 0px;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  background-color: #000;
  transition: height 0.2s ease;
}

.control-area {
  display: flex;
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
  display: flex;
  align-items: flex-start;
  margin-top: -12px;
  height: 32px;
  gap: 12px;
  align-self: stretch;
}

.title-block {
  display: flex;
  align-items: flex-start;
  align-content: flex-start;
  gap: 12px;
  flex: 1 0 0;
  align-self: stretch;
  flex-wrap: wrap;
}

.image-div {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  align-self: stretch;
}

.main-column {
  width: 180px;
  height: 180px;
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
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: flex-start;
  gap: 8px;
  flex: 1 0 0;
}

.state {
  display: flex;
  padding: 12px;
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;

  border-radius: var(--border-button-round, 8px);
  background: var(--4-base-dark-base, rgba(255, 255, 255, 0.07));
}

.key-info-div {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 12px;
  align-self: stretch;
}

.stretch {
  flex: 1 0 0;
}
</style>