<template>
  <div>
    <div v-for="prop in properties" :key="prop">
      <label>{{ prop }}:</label>
      <input v-model="item[prop]" @blur="emitUpdate" />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    itemId: String,
    item: Object
  },
  data() {
    return {
      properties: ['name', 'image', 'price', 'description']
    };
  },
  methods: {
    emitUpdate() {
      this.$emit('updateItem', this.itemId, this.item);
    }
  }
}
</script>

<style lang="scss" scoped>
.input {
  width: auto;
  padding: 12px;
  justify-content: space-between;
  align-items: center;
  border-radius: var(--border-content, 6px);
  background: var(--4-base-dark-base, rgba(255, 255, 255, 0.07));
}

.nav {
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}

.form-frame {
  width: 200px;
  min-width: 200px;
  flex-grow: 1;
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  gap: 4px;
}

.headline {
  font-size: 16px;
  font-weight: 500;
  line-height: 21px;
  color: var(--3-text-dark-2nd-white,
      var(--token-secondary-text, rgba(255, 255, 255, 0.75)));
}

.input {
  width: auto;
  padding: 12px;
  border: 0px;
  border-radius: var(--border-content, 6px);
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}

.input-on {
  width: auto;
  padding: 12px;
  border: 1px solid var(--baseline-green, #3dc363);
  border-radius: var(--border-content, 6px);
  box-sizing: border-box;
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}

// Temp

.temp-button {
  cursor: pointer;
  background-color: transparent;
  border: 0px;
  padding: 10px 16px;
  justify-content: center;
  align-items: center;
  border-radius: var(--border-button-round, 8px);
  background: var(--token-theme, #fafafa);
  color: var(--token-invert, #0e0d0f);

  font-family: Be Vietnam Pro;
  font-size: 15px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;
}

.text-button {
  cursor: pointer;
  color: var(--2-brand-gray, #808cab);
  background-color: transparent;
  padding: 0px;

  font-family: Be Vietnam Pro;
  font-size: 15px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;
}
</style>
