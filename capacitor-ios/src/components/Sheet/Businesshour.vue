<template>
  <div>
    <template v-if="viewMode === 'overview'">
      <div class="flex-col">
        <div>
          <p :class="['subhead', bizHr.stateClass]">{{ bizHr.state }}</p>
          <p :class="['subhead', bizHr.nextTimeClass]">&nbsp;·&nbsp;{{ bizHr.nextTime }}</p>
        </div>
      </div>
    </template>
    <!-- <template v-if="viewMode === 'detail'">
      <div class="frame">
        <div class="icon"></div>
        <p :class="['subhead', bizHr.stateClass]">{{ bizHr.state }}</p>
        <p class="_color-secondary subhead" v-if="bizHr.isTime">&nbsp;·&nbsp;{{ bizHr.time }}</p>
        <p :class="['subhead', bizHr.nextTimeClass]" v-if="bizHr.isNextTime">&nbsp;·&nbsp;{{ bizHr.nextTime }}</p>
        <p class="subhead">{{ bizHr.formattedBusinessHours }}</p>
      </div>
    </template> -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  bizTime: { type: Object, default: () => ({}) },
  viewMode: { type: String, default: 'overview' }
});

// Reactive current time
const currentTime = ref(new Date());

// Update time every minute
let timeUpdateInterval = null;
onMounted(() => {
  timeUpdateInterval = setInterval(() => {
    currentTime.value = new Date();
  }, 60000);
});
onUnmounted(() => {
  if (timeUpdateInterval) clearInterval(timeUpdateInterval);
});

// DST-safe offset calculation
function getOffsetMinutesForZone(tz, at = new Date()) {
  const fmt = new Intl.DateTimeFormat('en-US', {
    timeZone: tz,
    hour12: false, year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit'
  });
  const parts = Object.fromEntries(fmt.formatToParts(at).map(p => [p.type, p.value]));
  const asUTC = Date.UTC(+parts.year, +parts.month - 1, +parts.day, +parts.hour, +parts.minute);
  return Math.round((asUTC - at.getTime()) / 60000); // DST-safe
}

function timezoneGapMinutes(userTz, shopTz, at = new Date()) {
  return getOffsetMinutesForZone(shopTz, at) - getOffsetMinutesForZone(userTz, at);
}

// Format "MMDD" to "Month Day"
function formatMMDDToMonthDay(mmdd) {
  if (typeof mmdd !== 'string') return '';
  const clean = mmdd.replace(/\D/g, '').padStart(4, '0'); // ensure "MMDD"
  if (clean.length < 4) return '';
  const monthIdx = parseInt(clean.slice(0, 2), 10) - 1; // 0..11
  const day = parseInt(clean.slice(2, 4), 10);

  if (Number.isNaN(monthIdx) || Number.isNaN(day)) return '';
  if (monthIdx < 0 || monthIdx > 11 || day <= 0 || day > 31) return '';

  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  return `${monthNames[monthIdx]} ${day}`;
}

// Parse "HH:mm" to minutes
function parseHHmm(str) {
  const [h, m] = str.split(':').map(Number);
  return h * 60 + m;
}

// Format minutes to "HH:mm"
function formatTime(totalMinutes) {
  const m = ((totalMinutes % 1440) + 1440) % 1440;
  const h = Math.floor(m / 60);
  const mm = m % 60;
  return `${h.toString().padStart(2, '0')}:${mm.toString().padStart(2, '0')}`;
}

// Convert business hours to ranges
function processShopBusinessHours(biz, weekdayName) {
  const raw = biz?.hours?.[weekdayName] || [];
  return raw
    .map(({ start, end }) => {
      let startMinutes = parseHHmm(start);
      let endMinutes = parseHHmm(end);
      if (endMinutes <= startMinutes) endMinutes += 1440;
      return { start: startMinutes, end: endMinutes };
    })
    // Ascending sort by a numeric property
    .sort((a, b) => a.start - b.start);
}

const bizHr = computed(() => {
  // UI defaults
  let state = '';
  let stateClass = '';
  let nextTime = '';
  let nextTimeClass = '';

  let nextOpenDate = '';
  let nextOpenDate_formatted = '';
  let nextOpenDay = '';
  let nextOpenDay_formatted = '';
  let nextOpenTime = '';

  const biz = props.bizTime || {};

  // Adjust user time to match stores in different timezone
  const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const shopTimezone = biz.timezone;
  const adjustedUserTime = computed(() => {
    if (shopTimezone === userTimezone) return currentTime.value;

    const gap = timezoneGapMinutes(userTimezone, shopTimezone, currentTime.value);
    return new Date(currentTime.value.getTime() + gap * 60000);
  });

  const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const daysOfWeekFormatted = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const adjustedUserTimeInMinutes = computed(() => adjustedUserTime.value.getHours() * 60 + adjustedUserTime.value.getMinutes());
  const shopBusinessHoursInMinutes = computed(() => processShopBusinessHours(biz, daysOfWeek[adjustedUserTime.value.getDay()]));
  const previousShopBusinessHoursInMinutes = computed(() => processShopBusinessHours(biz, daysOfWeek[(adjustedUserTime.value.getDay() + 6) % 7]));
  const nextShopBusinessHoursInMinutes = computed(() => processShopBusinessHours(biz, daysOfWeek[(adjustedUserTime.value.getDay() + 1) % 7]));

  // Build "MMDD" from the adjusted (shop-local) time
  const adjustedUserMMDD =
    String(adjustedUserTime.value.getMonth() + 1).padStart(2, '0') +
    String(adjustedUserTime.value.getDate()).padStart(2, '0');

  // Normalize the holiday list to safe "MMDD" strings
  const holidays = Array.isArray(biz?.holiday)
    ? biz.holiday.map(h => String(h).replace(/\D/g, '').padStart(4, '0'))
    : [];
  const isHoliday = holidays.includes(adjustedUserMMDD);

  // Yesterday's business hours
  const isOpenFromYesterday = (() => {
    // move "now" into yesterday's extended frame
    const shiftedNow = adjustedUserTimeInMinutes.value + 1440;
    console.log("shiftedNow", shiftedNow);
    console.log("previousShopBusinessHoursInMinutes", previousShopBusinessHoursInMinutes.value);
    for (const r of previousShopBusinessHoursInMinutes.value) {
      // Only consider ranges that cross midnight (normalized end > 1440)
      if (r.end <= 1440) continue;
      if (shiftedNow >= r.start && shiftedNow < r.end) {
        const minsToClose = r.end - shiftedNow;
        const status = minsToClose < 30 ? 'closeSoon' : 'open';
        return { status, end: r.end, endFormatted: formatTime(r.end) };
      }
    }
    return { status: 'closed' };
  })();

  // // 🐞 Debug console
  console.log("userTimezone:", userTimezone);
  console.log("shopTimezone:", shopTimezone);
  console.log("userTime:", currentTime.value);
  console.log("adjustedUserTime:", adjustedUserTime.value);
  console.log("Days of Week:", daysOfWeek[adjustedUserTime.value.getDay()]);
  console.log("adjustedUserMMDD:", adjustedUserMMDD);
  console.log("holidays:", holidays);
  console.log("isHoliday:", isHoliday);
  console.log("---END---");


  // 1) 24hr logic
  if (biz?.['24hr'] === true) {
    if (!isHoliday) {
      state = 'Open 24H';
      stateClass = 'isOpen';

    } else {
      state = 'Closed for Holiday';
      stateClass = 'isHoliday';
      for (let i = 1; i <= 365; i++) {
        const checkDate = new Date(adjustedUserTime.value);
        checkDate.setDate(checkDate.getDate() + i);

        const checkMMDD =
          String(checkDate.getMonth() + 1).padStart(2, '0') +
          String(checkDate.getDate()).padStart(2, '0');

        if (!holidays.includes(checkMMDD)) {
          // Found a non-holiday
          nextOpenDate = checkMMDD;
          nextOpenDate_formatted = formatMMDDToMonthDay(nextOpenDate);
          nextOpenDay = daysOfWeek[checkDate.getDay()];
          nextOpenDay_formatted = daysOfWeekFormatted[checkDate.getDay()];
          const ranges = processShopBusinessHours(biz, nextOpenDay);
          if (ranges.length > 0) {
            nextOpenTime = formatTime(ranges[0].start);
          }
          nextTime = 'Opens ' + nextOpenDay_formatted + ', ' + nextOpenDate_formatted + ' at ' + nextOpenTime;
          nextTimeClass = 'isDefault';
          break;
        }
      }
    }
    return {
      state,
      stateClass,
      nextTime,
      nextTimeClass,
    };
  }

  // 2) Holiday logic
  // For previous day overnight ranges, compare (now + 1440) to previous ranges
  if (isHoliday && previousShopBusinessHoursInMinutes.value.length === 0) {
    state = 'Closed for Holiday';
    stateClass = 'isHoliday';
    for (let i = 1; i <= 365; i++) {
      const checkDate = new Date(adjustedUserTime.value);
      checkDate.setDate(checkDate.getDate() + i);

      const checkMMDD =
        String(checkDate.getMonth() + 1).padStart(2, '0') +
        String(checkDate.getDate()).padStart(2, '0');

      if (!holidays.includes(checkMMDD)) {
        // Found a non-holiday
        nextOpenDate = checkMMDD;
        nextOpenDate_formatted = formatMMDDToMonthDay(nextOpenDate);
        nextOpenDay = daysOfWeek[checkDate.getDay()];
        nextOpenDay_formatted = daysOfWeekFormatted[checkDate.getDay()];
        const ranges = processShopBusinessHours(biz, nextOpenDay);
        if (ranges.length > 0) {
          nextOpenTime = formatTime(ranges[0].start);
        }
        nextTime = 'Opens ' + nextOpenDay_formatted + ', ' + nextOpenDate_formatted + ' at ' + nextOpenTime;
        nextTimeClass = 'isDefault';
        break;
      }
    }
    return {
      state,
      stateClass,
      nextTime,
      nextTimeClass
    };
  }

  if (isHoliday && previousShopBusinessHoursInMinutes.value.length > 0) {
    console.log("isOpenFromYesterday", isOpenFromYesterday);
    if (isOpenFromYesterday.status === 'open') {
      state = 'Open';
      stateClass = 'isOpen';
      nextTime = 'Closes at ' + isOpenFromYesterday.endFormatted;
      nextTimeClass = 'isDefault';
      return {
        state,
        stateClass,
        nextTime,
        nextTimeClass,
      };
    } else if (isOpenFromYesterday.status === 'closeSoon') {
      state = 'Close Soon';
      stateClass = 'isBetween';
      nextTime = 'Close at ' + isOpenFromYesterday.endFormatted;
      nextTimeClass = 'isDefault';
      return {
        state,
        stateClass,
        nextTime,
        nextTimeClass,
      };
    } else {
      state = 'Closed';
      stateClass = 'isClosed';
      for (let i = 1; i <= 365; i++) {
        const checkDate = new Date(adjustedUserTime.value);
        checkDate.setDate(checkDate.getDate() + i);

        const checkMMDD =
          String(checkDate.getMonth() + 1).padStart(2, '0') +
          String(checkDate.getDate()).padStart(2, '0');

        if (!holidays.includes(checkMMDD)) {
          nextOpenDate = checkMMDD;
          nextOpenDate_formatted = formatMMDDToMonthDay(nextOpenDate);
          nextOpenDay = daysOfWeek[checkDate.getDay()];
          nextOpenDay_formatted = daysOfWeekFormatted[checkDate.getDay()];
          const ranges = processShopBusinessHours(biz, nextOpenDay);
          if (ranges.length > 0) {
            nextOpenTime = formatTime(ranges[0].start);
          }
          nextTime = 'Opens ' + nextOpenDay_formatted + ', ' + nextOpenDate_formatted + ' at ' + nextOpenTime;
          nextTimeClass = 'isDefault';
          break;
        }
      }
      return {
        state,
        stateClass,
        nextTime,
        nextTimeClass,
      };
    }
  }

  // 3) General logic
  if (!isHoliday && shopBusinessHoursInMinutes.value.length > 0) {
    if (isOpenFromYesterday.status === 'open') {
      state = 'Open';
      stateClass = 'isOpen';
      nextTime = 'Closes at ' + isOpenFromYesterday.endFormatted;
      nextTimeClass = 'isDefault';
      return {
        state,
        stateClass,
        nextTime,
        nextTimeClass,
      };
    } else if (isOpenFromYesterday.status === 'closeSoon') {
      state = 'Close Soon';
      stateClass = 'isBetween';
      nextTime = 'Close at ' + isOpenFromYesterday.endFormatted;
      nextTimeClass = 'isDefault';
      return {
        state,
        stateClass,
        nextTime,
        nextTimeClass,
      };
    } else {
      state = 'Closed';
      stateClass = 'isClosed';
      for (let i = 1; i <= 365; i++) {
        const checkDate = new Date(adjustedUserTime.value);
        checkDate.setDate(checkDate.getDate() + i);

        const checkMMDD =
          String(checkDate.getMonth() + 1).padStart(2, '0') +
          String(checkDate.getDate()).padStart(2, '0');

        if (!holidays.includes(checkMMDD)) {
          nextOpenDate = checkMMDD;
          nextOpenDate_formatted = formatMMDDToMonthDay(nextOpenDate);
          nextOpenDay = daysOfWeek[checkDate.getDay()];
          nextOpenDay_formatted = daysOfWeekFormatted[checkDate.getDay()];
          const ranges = processShopBusinessHours(biz, nextOpenDay);
          if (ranges.length > 0) {
            nextOpenTime = formatTime(ranges[0].start);
          }
          nextTime = 'Opens ' + nextOpenDay_formatted + ', ' + nextOpenDate_formatted + ' at ' + nextOpenTime;
          nextTimeClass = 'isDefault';
          break;
        }
      }
      return {
        state,
        stateClass,
        nextTime,
        nextTimeClass,
      };
    }
  } else {
    state = 'OPNNNNNNN!';

    // for (const r of previousShopBusinessHoursInMinutes.value) {
    //   if (adjustedUserTimeInMinutes.value < (r.end + 1440)) {
    //     state = 'Open';
    //     stateClass = 'isOpen';

    //     // 🐞 Debug console
    //     console.log("state in for loop", state);
    //     console.log("stateClass in for loop", stateClass);
    //     console.log("adjustedUserTimeInMinutes", adjustedUserTimeInMinutes.value);
    //     console.log("shopBusinessHoursInMinutes", shopBusinessHoursInMinutes.value);

    //     break;
    //   } else {
    //     state = 'Closed';
    //     stateClass = 'isClosed';
    //   }
    // }

  }
  // // If no business hours today and yesterday
  // const noHoursAnywhere = [
  //   shopBusinessHoursInMinutes.value,
  //   previousShopBusinessHoursInMinutes.value,
  // ].every(r => r.length === 0);

  // if (!previousShopBusinessHoursInMinutes.value.length) {



  //   state = 'Closed';
  //   stateClass = 'isClosed';
  //   return {
  //     state,
  //     stateClass,
  //     nextTime,
  //     nextTimeClass,
  //     // 🏗️ Not yet
  //     // 🐞 Debug console
  //     userTimezone: userTimezone,
  //     shopTimezone: shopTimezone,
  //     userTime: currentTime.value,
  //     adjustedUserTime: adjustedUserTime.value
  //   };
  // }


  // for (let i = 1; i <= 365; i++) {
  //       const checkDate = new Date(adjustedUserTime.value);
  //       checkDate.setDate(checkDate.getDate() + i);

  //       const checkMMDD =
  //         String(checkDate.getMonth() + 1).padStart(2, '0') +
  //         String(checkDate.getDate()).padStart(2, '0');

  //       if (!holidays.includes(checkMMDD)) {
  //         // Found a non-holiday
  //         nextOpenDate = checkMMDD;
  //         nextOpenDate_formatted = formatMMDDToMonthDay(nextOpenDate);
  //         nextOpenDay = daysOfWeek[checkDate.getDay()];
  //         nextOpenDay_formatted = daysOfWeekFormatted[checkDate.getDay()];
  //         const ranges = processShopBusinessHours(biz, nextOpenDay);
  //         if (ranges.length > 0) {
  //           nextOpenTime = formatTime(ranges[0].start);
  //         }
  //         nextTime = 'Opens ' + nextOpenDay_formatted + ', ' + nextOpenDate_formatted + ' at ' + nextOpenTime;
  //         nextTimeClass = 'isDefault';
  //         break;
  //       }
  //     }




  // // Check if open now
  // for (const r of shopBusinessHoursInMinutes.value) {
  //   if (adjustedUserTimeInMinutes.value >= r.start && adjustedUserTimeInMinutes.value < r.end) {
  //     state = 'Open';
  //     stateClass = 'isOpen';

  //     // 🐞 Debug console
  //     console.log("state in for loop", state);
  //     console.log("stateClass in for loop", stateClass);
  //     console.log("adjustedUserTimeInMinutes", adjustedUserTimeInMinutes.value);
  //     console.log("shopBusinessHoursInMinutes", shopBusinessHoursInMinutes.value);

  //     break;
  //   } else {
  //     state = 'Closed';
  //     stateClass = 'isClosed';
  //   }
  // }


  return {
    state,
    nextTime: '',
    stateClass,
    nextTimeClass: 'isDefault',
    // Debug
    userTimezone: userTimezone,
    shopTimezone: shopTimezone,
    userTime: currentTime.value,
    adjustedUserTime: adjustedUserTime.value
  }
});
</script>

<style lang="scss" scoped>
.isHoliday {
  color: #ce53fa;
}

.isClosed {
  color: #FF7ABD;
}

.isOpen {
  color: #3dc363;
}

.isBetween {
  color: #F8BA1B;
}

.isDefault {
  color: var(--primary-text);
}

.frame {
  align-items: flex-start;
  gap: 8px;
  align-self: stretch;
}

.icon {
  min-width: 24px;
  height: 24px;
  background: url("/icon/info/time.png") no-repeat center/contain;
}
</style>