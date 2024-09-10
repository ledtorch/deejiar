<template>
  <div class="thumbnail-frame flex-col" :style="backgroundStyle">
    <div class="base">
      <p class="caption2">No.{{ ranking }}</p>
    </div>
    <div class="base">
      <p class="caption1">{{ title }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  bar: {
    type: Object,
    required: true
  }
});
const ranking = props.bar.properties.id;
const title = props.bar.properties.title;

const backgroundStyle = computed(() => {
  // 🐞 debug console
  console.log(props.bar);
  const imagePath = props.bar.properties.item1.image;
  return {
    backgroundImage: imagePath ? `url(/${imagePath})` : 'none',
    backgroundSize: 'cover',
    backgroundPosition: 'center'
  };
});
</script>

<style lang="scss" scoped>
.thumbnail-frame {
  min-width: 120px;
  min-height: 120px;

  padding: 4px;
  border-radius: 8px;
  background: lightgray 50%;

  justify-content: space-between;
  align-items: flex-start;

}

.minimize-button {
  position: absolute;
  top: 12px;
  right: 12px;
}

.base {
  padding: var(--Atom, 2px) var(--Unit, 4px);
  flex-direction: column;
  align-items: flex-start;
  border-radius: var(--Round-Mini, 4px);
  background: var(--Base-Invert-base, rgba(0, 0, 0, 0.60));
}
</style>