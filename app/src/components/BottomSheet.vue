<template>
  <div class="bottom-sheet" :class="{ open: isOpen }">
    <div class="handle" @click="toggle"></div>
    <div class="content">
      <slot></slot>
    </div>
  </div>
</template>
  
  <script>
export default {
  data() {
    return {
      isOpen: false,
    };
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen;
    },
  },
};
</script>
  
  <style>
.bottom-sheet {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 70px;
  overflow: hidden;
  transition: height 0.3s ease;
  display: flex;
  width: 100px; /* Added */
  padding: 12px 16px 16px 16px; /* Added */
  flex-direction: column; /* Added */
  align-items: center; /* Added */
  gap: 8px; /* Added */
  border-radius: 12px 12px 0px 0px; /* Updated */
  background: var(--1-system-black, #000); /* Updated */
}

.bottom-sheet.open {
  height: 300px; /* You can adjust this value to fit your content */
}

.handle {
  height: 8px;
  width: 40px;
  margin: 8px auto;
  background-color: #cccccc;
  border-radius: 4px;
  cursor: pointer;
}

.content {
  padding: 16px;
  overflow-y: auto;
}
</style>
  