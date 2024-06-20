<template>
  <div class="flex-col form-frame-businesshour">
    <div class="nav">
      <p class="headline">JSON data</p>
      <button class="text-button" v-if="!editing" @click="edit(property)">Edit</button>
      <button class="text-button" v-if="editing" @click="save">Save</button>
    </div>
    <textarea v-model="businesshourString" class="full-size"></textarea>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  businesshour: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['update']);
const businesshourString = ref(JSON.stringify(props.businesshour, null, 2));
const editing = ref(false);

watch(() => props.businesshour, (newVal) => {
  if (!editing.value) {
    businesshourString.value = JSON.stringify(newVal, null, 2);
  }
});

const edit = () => {
  editing.value = true;
};

const save = () => {
  let updatedBusinessHour;
  try {
    updatedBusinessHour = JSON.parse(businesshourString.value);
  } catch (e) {
    console.error('Invalid JSON:', e);
    return;
  }
  emit('update', updatedBusinessHour);
  editing.value = false;
};
</script>

<style lang="scss" scoped>
.form-frame-businesshour {
  width: 100%;
  height: 400px;
  flex-grow: 1;
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  gap: 4px;
}

.full-size {
  width: 100%;
  height: 100%;

  /* Optional: Disables the resize handle */
  resize: none;
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

.headline {
  font-size: 16px;
  font-weight: 500;
  line-height: 21px;
  color: var(--3-text-dark-2nd-white,
      var(--token-secondary-text, rgba(255, 255, 255, 0.75)));
}

.nav {
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}
</style>