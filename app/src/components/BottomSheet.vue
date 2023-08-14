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
import { ref, onMounted, onBeforeUnmount } from "vue";

import IconButtonClose from "./Button/IconButtonClose.vue";
import TagShopType from "./Button/TagShopType.vue";
import { useRouter } from "vue-router";

export default {
  components: { IconButtonClose, TagShopType },
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
    const isDragging = ref(false);
    const bottomSheetHeight = ref("32px"); // Default height
    const bottomSheet = ref(null);
    const router = useRouter();
    const controlArea = ref(null);
    let lastY = 0;
    const someMinHeight = 32;
    const someMaxHeight = 467;
    const startDragging = (event) => {
      isDragging.value = true;
      event.preventDefault(); // Prevent default action for touch devices
    };
    const drag = (event) => {
      if (!isDragging.value) return;
      // Use clientY for touch events
      const movementY =
        event instanceof MouseEvent
          ? event.movementY
          : event.touches[0].clientY - lastY;
      lastY = event.touches ? event.touches[0].clientY : event.clientY;
      const currentHeight = parseFloat(bottomSheetHeight.value);
      const newHeight = currentHeight - movementY;
      if (newHeight >= someMaxHeight) {
        bottomSheetHeight.value = "600px"; // or another desired value
        const storeTitle = encodeURIComponent(this.store.properties.title);
        router.push(`/store/${storeTitle}`);
      } else {
        bottomSheetHeight.value =
          Math.max(someMinHeight, Math.min(someMaxHeight, newHeight)) + "px";
      }
      if (newHeight >= someMaxHeight) {
        const storeTitle = encodeURIComponent(this.store.properties.title);
        router.push(`/store/${storeTitle}`);
      }
    };
    const stopDragging = () => {
      isDragging.value = false;
    };
    onMounted(() => {
      controlArea.value.addEventListener("mousedown", startDragging);
      controlArea.value.addEventListener("touchstart", startDragging, {
        passive: false,
      });
      window.addEventListener("mousemove", drag);
      window.addEventListener("touchmove", drag, { passive: false });
      window.addEventListener("mouseup", stopDragging);
      window.addEventListener("touchend", stopDragging);
    });
    onBeforeUnmount(() => {
      window.removeEventListener("mousemove", drag);
      window.removeEventListener("mouseup", stopDragging);
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
  },
};
</script>


<style scoped>
.bottom-sheet {
  display: flex;
  width: 390px;
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
/* Local Prefix */
</style>
