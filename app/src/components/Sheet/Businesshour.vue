<template>
  <div>
    <p :class="[businessHoursClass, 'subhead']">{{ businessHours }}</p>
    <!-- <p>{{ currentMonthandDay }}</p> -->
  </div>
</template>
  
<script>
export default {
  props: {
    store: Object,
  },
  computed: {
    businessHours() {
      // ↓ Define time
      const currentTime = new Date();
      let currentDay = currentTime.getDay(); // Sunday = 0
      if (currentDay === 0) currentDay = 7; // If Sunday, make it 7
      const currentMonth = String(currentTime.getMonth() + 1).padStart(2, "0"); // Jan = 0
      const currentDate = String(currentTime.getDate()).padStart(2, "0");
      const currentHour = String(currentTime.getHours()).padStart(2, "0");
      const currentMinute = String(currentTime.getMinutes()).padStart(2, "0");

      // // ↓ 🐞 Debug console
      // console.log("Day: " + currentDay)
      // console.log("Month: " + currentMonth)
      // console.log("Date: " + currentDate)
      // console.log("Hour: " + currentHour)
      // console.log("Minute: " + currentMinute)

      const holidays = this.store.businesshour[0].Holiday;
      // console.log("Holidays: " + holidays); // ← 🐞 Debug console
      // Extract holiday

      // ↓ Check if the business is closed for the holiday
      const currentMonthandDay = currentMonth + currentDate;
      if (holidays.includes(currentMonthandDay)) {
        return "Closed for Holiday";
      }

      // ↓ Check if closed today
      const bizDay = this.store.businesshour[currentDay];
      // console.log("Business Day: " + bizDay); // ← 🐞 Debug console
      if (bizDay == null) {
        return "Closed";
      }

      // return `${currentDay}:${currentMonth}:${currentDate}:${currentHour}:${currentMinute}`;
    },
    businessHoursClass() {
      if (this.businessHours === "Closed for Holiday") {
        return "closed-for-holiday";
      } else if (this.businessHours === "Closed") {
        return "closed";
      }
      return ""; // Default class if none of the conditions are met
    },
  },
};
</script>
  
<style scoped>
.closed-for-holiday {
  color: #ce53fa;
}

.closed {
  color: #fd435f;
}
</style>

