<template>
  <div class="form-frame">
    <div class="nav">
      <p class="headline">{{ capitalizedProperty }}</p>
      <!-- Only show the Edit button when editing is false -->
      <button class="text-button" v-if="!editing" @click="edit(property)">Edit</button>
      <!-- Only show the Save button when editing is true -->
      <button class="text-button" v-if="editing" @click="save">Save</button>
    </div>
    <input :class="{ input: !editing, 'input-on': editing }" v-model="editingValue" />
  </div>
</template>

<script>
export default {
  props: ['value', 'property'],
  data() {
    return {
      editing: false,
      editingValue: this.value,
    };
  },
  computed: {
    // Convert the key to the title
    capitalizedProperty() {
      // // 🐞 Debug console
      // console.log('The value: ' + this.value);
      // console.log('The property: ' + this.property);

      return this.property.charAt(0).toUpperCase() + this.property.slice(1);
    },
  },
  methods: {
    edit() {
      // // 🐞 Debug console
      // console.log('Start editing');
      // console.log('value:', this.value);
      // console.log('property:', this.property);
      // console.log('editingValue:', this.editingValue);

      this.editing = true;
      this.editingValue = this.value;
    },
    save() {
      let valueToEmit;
      valueToEmit = this.editingValue;
      this.$emit("update", [this.property, valueToEmit]);
      this.editing = false;

      // 🐞 Debug console 
      console.log('valueToEmit:', valueToEmit);
    }
  },
};
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

.input,
.input-on {
  width: auto;
  padding: 12px;
  border: 1px solid transparent;
  /* Ensures border width is included in height calculations */
  border-radius: var(--border-content, 6px);
  box-sizing: border-box;
  /* Includes padding and border in the element's total width and height */
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
  height: 50px;
  /* Explicitly setting the height */
}

.input-on {
  border: 1px solid var(--baseline-green, #3dc363);
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
