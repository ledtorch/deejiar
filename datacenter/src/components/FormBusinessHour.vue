<template>
  <div class="business-hours">
    <h4>Business Hours</h4>
    <div v-for="(day, index) in businesshour" :key="index" class="day-entry">
      <div v-for="(value, key) in day" :key="key" class="day-wrapper">
        <h5>{{ key }}</h5>
        <div v-if="Array.isArray(value)">
          <div v-for="(slot, slotIndex) in value" :key="slotIndex" class="slot-entry">
            <label>Start</label>
            <input type="time" v-model="slot.Start"
              @input="updateBusinessHour(index, key, slotIndex, 'Start', slot.Start)">
            <label>Finish</label>
            <input type="time" v-model="slot.Finish"
              @input="updateBusinessHour(index, key, slotIndex, 'Finish', slot.Finish)">
            <button @click="removeSlot(index, key, slotIndex)">Remove Slot</button>
          </div>
          <button @click="addSlot(index, key)">Add Slot</button>
        </div>
        <div v-else>
          <input type="checkbox" v-model="day[key]" @change="updateBusinessHour(index, key, null, null, day[key])">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  businesshour: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['update', 'update-slot', 'add-slot', 'remove-slot']);

const updateBusinessHour = (dayIndex, dayKey, slotIndex, slotKey, value) => {
  if (slotIndex === null) {
    emit('update', [dayIndex, dayKey, value]);
  } else {
    emit('update-slot', [dayIndex, dayKey, slotIndex, slotKey, value]);
  }
};

const addSlot = (dayIndex, dayKey) => {
  emit('add-slot', [dayIndex, dayKey]);
};

const removeSlot = (dayIndex, dayKey, slotIndex) => {
  emit('remove-slot', [dayIndex, dayKey, slotIndex]);
};
</script>