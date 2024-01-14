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
      <div class="frame">
        <div class="icon"></div>
        <p class="subhead">{{ bizHr.currentDayName }}</p>
        <p class="subhead">{{ bizHr.formattedBusinessHours }}</p>
      </div>
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

      const currentDate = currentTime.toLocaleDateString('en-US', { month: '2-digit', day: '2-digit' }).replace('/', '');
      const currentHour = String(currentTime.getHours());
      const currentMinute = String(currentTime.getMinutes());
      const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
      const currentDayName = daysOfWeek[currentDay - 1];
      // let timeRanges = [];
      let formattedTimeRanges = [];
      let displayStartHour = "";
      let displayStartMinute = "";
      let displayFinishHour = "";
      let displayFinishMinute = "";

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
      // console.log("currentDayName: " + currentDayName)
      // console.log("MMDD: " + currentDate)
      // console.log("Hour: " + currentHour)
      // console.log("Minute: " + currentMinute)

      if (this.bizTime[0]?.['24hr']) {
        state = "Open 24H";
        stateClass = "isOpen";
      }

      // Check for holiday
      else if (this.bizTime[0]?.['Holiday']?.includes(currentDate)) {
        state = "Closed for Holiday";
        stateClass = "isHoliday";
        // 🏗️ TODO:
        // Next Time
      }

      else if (this.bizTime[currentDay] === false) {
        state = "Closed";
        stateClass = "isClose";

        // 🏗️ TODO:
        // Next Time
      }

      else {
        // Access the object containing the business hours for the current day
        const currentBizHrObj = this.bizTime[currentDay];

        if (currentBizHrObj !== false && currentBizHrObj[currentDayName]) {
          const currentBizHr = currentBizHrObj[currentDayName];
          // // 🐞 Debug console
          // console.log('currentBizHr: ', currentBizHr);

          /* 
            Get the current time in minutes and convert to minutes to calculate
            For example, 0602 = 6*60(minutes) + 2 = 362
          */
          const currentTimeInMinutes = parseInt(currentHour) * 60 + parseInt(currentMinute);
          // 🐞 Debug console
          console.log('currentTimeInMinutes', currentTimeInMinutes);

          // Initialize a variable to keep track of the closest opening time
          let closestOpeningTimeInMinutes = Infinity;

          // Iterate through the time ranges for the current day
          for (let i = 0; i < currentBizHr.length; i++) {
            const timeRange = currentBizHr[i];
            const startHourMinute = timeRange.Start;
            const finishHourMinute = timeRange.Finish;

            // Convert start and finish times to Int
            const startHour = parseInt(startHourMinute.slice(0, 2));
            const startMinute = parseInt(startHourMinute.slice(2));
            const finishHour = parseInt(finishHourMinute.slice(0, 2));
            const finishMinute = parseInt(finishHourMinute.slice(2));
            // Convert above value to minutes
            const startTimeInMinutes = startHour * 60 + startMinute;
            const finishTimeInMinutes = finishHour * 60 + finishMinute;

            // Create a time range object
            let timeRangeObj = {
              displayStartHour: startHourMinute.slice(0, 2),
              displayStartMinute: startHourMinute.slice(2),
              displayFinishHour: finishHourMinute.slice(0, 2),
              displayFinishMinute: finishHourMinute.slice(2)
            };

            // Format the current time range
            let formattedTimeRange = `${timeRangeObj.displayStartHour}:${timeRangeObj.displayStartMinute} - ${timeRangeObj.displayFinishHour}:${timeRangeObj.displayFinishMinute}`;


            // Add the formatted time range to the formattedTimeRanges array
            formattedTimeRanges.push(formattedTimeRange);

            // Check if the current time is within this time range
            if (currentTimeInMinutes >= startTimeInMinutes && currentTimeInMinutes <= finishTimeInMinutes) {
              state = "Opening";
              time = finishTimeInMinutes - currentTimeInMinutes;  // Time remaining until closing
              stateClass = "isOpen";
              break;  // Exit the loop as the current time is within the business hours
            }

            // Update the closest opening time if the current time is before this time range
            if (currentTimeInMinutes < startTimeInMinutes) {
              closestOpeningTimeInMinutes = Math.min(closestOpeningTimeInMinutes, startTimeInMinutes);
            }
          }

          // If the state hasn't been set to "Opening", the business is closed
          if (!state) {
            state = "Closed";
            stateClass = "isClose";

            // 🏗️ TODO:
            // Next Time
          }
        } else {
          // Handle the case where business hours for the current day are not found
          state = "Closed";
          stateClass = "isClose";
        }
      }
      let formattedBusinessHours = formattedTimeRanges.join(', ');
      return {
        state: state,
        time: time,
        isTime: isTime,
        nextTime: nextTime,
        isNextTime: isNextTime,
        stateClass: stateClass,
        timeClass: timeClass,
        nextTimeClass: nextTimeClass,
        currentDayName: currentDayName,
        // timeRanges: timeRanges,
        formattedBusinessHours: formattedBusinessHours
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

.frame {
  align-items: flex-start;
  gap: 8px;
  align-self: stretch;
}

.icon {
  min-width: 24px;
  height: 24px;
  background: url("/Icon/Info/Time.png") no-repeat center/contain;
}
</style>