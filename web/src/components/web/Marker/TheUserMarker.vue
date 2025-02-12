<template>
  <div class="frame" :style="markerStyle">
    <div class="ring">
      <div class="core"></div>
    </div>
  </div>
</template>

<script setup>
// import { computed } from 'vue';

// const props = defineProps({
//   position: {
//     type: Object,
//     required: true
//   }
// });

// const markerStyle = computed(() => ({
//   position: 'absolute',
//   left: `${props.position.x}px`,
//   top: `${props.position.y}px`,
//   transform: 'translate(-50%, -50%)'
// }));
</script>

<style lang="scss" scoped>
.frame {
  position: relative;
  width: 24px;
  height: 24px;
  transform: translate(-50%, -50%);
}

.ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 19px;
  height: 19px;
  border-radius: 20px;
  border: 1px dashed var(--Color-Primary, rgba(255, 255, 255, 0.95));
  box-shadow: none;
  animation: rotate360 6000ms linear infinite;
}

.core {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 10px;
  height: 10px;
  border-radius: 16px;
  background: var(--Color-Primary, rgba(255, 255, 255, 0.95));
  animation: breath 3000ms ease-in-out infinite;
  animation-delay: 200ms;
}

@keyframes rotate360 {
  from {
    transform: translate(-50%, -50%) rotate(0deg);
  }

  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

@keyframes breath {
  0% {
    width: 12px;
    height: 12px;
  }

  50% {
    width: 14px;
    height: 14px;
  }

  100% {
    width: 12px;
    height: 12px;
  }
}
</style>