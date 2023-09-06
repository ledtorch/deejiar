<!-- <template>
  <div>
    <p :class="['subhead', bizHr.stateClass]">{{ bizHr.state }}</p>
    <p :class="['subhead', bizHr.timeClass]" v-if="bizHr.isTime">&nbsp; · &nbsp;{{ bizHr.time }}</p>
    <p
      :class="['subhead', bizHr.nextTimeClass]"
      v-if="bizHr.isNextTime"
    >&nbsp; · &nbsp;{{ bizHr.nextTime }}</p>
  </div>
</template> -->

<template>
  <div>
    <template v-if="viewMode === 'overview'">
      <div>
        <p :class="['subhead', bizHr.stateClass]">{{ bizHr.state }}</p>
        <p :class="['subhead', bizHr.timeClass]" v-if="bizHr.isTime">&nbsp; · &nbsp;{{ bizHr.time }}</p>
        <p :class="['subhead', bizHr.nextTimeClass]" v-if="bizHr.isNextTime">&nbsp; · &nbsp;{{ bizHr.nextTime }}</p>
      </div>
    </template>

    <template v-if="viewMode === 'detail'">
      <div class="icon"></div>
      <p class="body">{{ time }}</p>
    </template>
  </div>
</template>


<script>
export default {
  props: {
    // DEBUG: It's obj when it's passed by BottomSheet.vue but array when it's passed by Detail.vue
    bizTime: '',
    viewMode: String
  },
  computed: {
    bizHr() {
      // Define time
      const currentTime = new Date();

      // If Sunday, make it 7 instead of 0
      let currentDay = currentTime.getDay();
      if (currentDay === 0) currentDay = 7;

      const currentMonth = String(currentTime.getMonth() + 1).padStart(2, "0");
      const currentDate = String(currentTime.getDate()).padStart(2, "0");
      const currentHour = String(currentTime.getHours()).padStart(2, "0");
      const currentMinute = String(currentTime.getMinutes()).padStart(2, "0");

      // Initialization
      let state = "";
      let time = "";
      let isTime = false;
      let nextTime = "";
      let isNextTime = false;
      let stateClass = "";
      let timeClass = "";
      let nextTimeClass = "";

      // // 🐞 Debug console
      // console.log("Day: " + currentDay)
      // console.log("Month: " + currentMonth)
      // console.log("Date: " + currentDate)
      // console.log("Hour: " + currentHour)
      // console.log("Minute: " + currentMinute)

      if (this.bizTime === null) {
        state = "Open 24H";
        stateClass = "isOpen";
      } else if (
        this.bizTime[0] &&
        this.bizTime[0].Holiday === null
      ) {
        state = "Open";
        stateClass = "isOpen";
      } else if (
        this.bizTime[0] &&
        this.bizTime[0].Holiday !== null
      ) {
        // Extract holiday
        const holidays = this.bizTime[0].Holiday;

        // // 🐞 Debug console
        // console.log("Holidays: " + holidays);

        // Check if the business is closed for the holiday
        const currentMonthandDay = currentMonth + currentDate;
        const bizDay = this.bizTime[currentDay];
        if (holidays.includes(currentMonthandDay)) {
          // Check for next open day after holiday
          let nextOpenDate = new Date(currentTime);
          let nextMonthAndDate;
          do {
            nextOpenDate.setDate(nextOpenDate.getDate() + 1); // Increment date by 1
            nextMonthAndDate =
              String(nextOpenDate.getMonth() + 1).padStart(2, "0") +
              String(nextOpenDate.getDate()).padStart(2, "0");
          } while (holidays.includes(nextMonthAndDate));

          state = "Closed for Holiday";
          stateClass = "isHoliday";
          nextTime = ` Reopens ${nextMonthAndDate}`;
          isNextTime = true;
        } else if (bizDay === null) {
          state = "Closed";
          stateClass = "isClose";

          // TODO: Reopen
        } else {
          state = "Open";
          stateClass = "isOpen";

          // TODO: Check time range
        }
      }

      return {
        state: state,
        time: time,
        isTime: isTime,
        nextTime: nextTime,
        isNextTime: isNextTime,
        stateClass: stateClass,
        timeClass: timeClass,
        nextTimeClass: nextTimeClass
      };
    }
  }
};
</script>
  
<style lang="scss" scoped>
.isHoliday {
  color: #ce53fa;
}

.isClose {
  color: #fd435f;
}

.isOpen {
  color: #3dc363;
  font-weight: 700;
}

.icon {
  width: 24px;
  height: 24px;
  background: url("/Icon/Info/Time.png") no-repeat center/contain;
}
</style>