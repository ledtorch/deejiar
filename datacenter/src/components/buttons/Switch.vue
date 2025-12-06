<template>
  <main class="switch-container">
    <div class="nav">
      <p class="_subtitle the-title">{{ title }}</p>
    </div>

    <div class="button-set-container">
      <button type="button" class="seg" :class="{ active: value === leftText }" @click="emit('update', leftText)">
        {{ leftText }}
      </button>

      <button type="button" class="seg" :class="{ active: value === rightText }" @click="emit('update', rightText)">
        {{ rightText }}
      </button>
    </div>
  </main>
</template>

<script setup>
const props = defineProps({
  leftText: { type: String, default: 'food' },
  rightText: { type: String, default: 'view' },
  title: { type: String, default: '?' },
  value: { type: String, default: '' },
});

const emit = defineEmits(['update']);
</script>


<style scoped lang="scss">
.button-set-container {
  align-items: center;
  gap: 6px;
  height: 46px;
  width: 100%;
  padding: 4px;
  border-radius: 6px;
  background: var(--base);
}

.seg {
  flex: 1;
  border: 0;
  padding: 8px 14px;
  border-radius: var(--Round-S, 4px);
  font-weight: 700;
  font-size: 14px;
  background: transparent;
  color: var(--secondary-text);
  cursor: pointer;
  transition: all 0.2s ease;

  &.active {
    height: 38px;
    border-radius: var(--Round-S, 4px);
    background: var(--Color-Primary, rgba(0, 0, 0, 0.95));
    color: #fff;
  }

  &:hover {
    background: rgba(0, 0, 0, 0.8);
    color: #fff;
  }
}

.nav {
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
  height: 24px;
}

.the-title {
  height: 22px;
  line-height: 22px;
  padding: 0px 4px;
  color: var(--secondary-text);
}

.switch-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 4px;
}
</style>
