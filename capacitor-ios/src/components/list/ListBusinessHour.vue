<template>
  <div>
    <template v-if="viewMode === 'overview'">
      <div>
        <p :class="[bizHr.stateClass, '_body2']">{{ bizHr.state }}</p>
        <p :class="[bizHr.nextTimeClass, '_body2']">&nbsp;·&nbsp;{{ bizHr.nextTime }}</p>
      </div>
    </template>
    <!-- 🏗️ TODO: Detail View -->
    <template v-if="viewMode === 'detail'">
      <div class="list-container">
        <img :src="iconSrc" class="icon">
        <div>
          <p :class="[bizHr.stateClass, '_body2']">{{ bizHr.state }}</p>
          <p :class="[bizHr.nextTimeClass, '_body2']">&nbsp;·&nbsp;{{ bizHr.nextTime }}</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import iconTimeLight from '@/assets/icons/store-info/time-light.svg'
import iconTimeDark from '@/assets/icons/store-info/time-dark.svg'

const iconSrc = computed(() => {
  return iconTimeDark
})

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
  const adjustedUserYesterday = computed(() => {
    const yesterday = new Date(adjustedUserTime.value)
    yesterday.setDate(yesterday.getDate() - 1)
    return yesterday
  })

  // Turn business hours to 0 - 1440 format
  const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const daysOfWeekFormatted = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const adjustedUserTimeInMinutes = computed(() => adjustedUserTime.value.getHours() * 60 + adjustedUserTime.value.getMinutes());
  const shopBusinessHoursInMinutes = computed(() => processShopBusinessHours(biz, daysOfWeek[adjustedUserTime.value.getDay()]));
  const previousShopBusinessHoursInMinutes = computed(() => processShopBusinessHours(biz, daysOfWeek[(adjustedUserTime.value.getDay() + 6) % 7]));

  // Build "MMDD" from the adjusted (shop-local) time
  const adjustedUserMMDD =
    String(adjustedUserTime.value.getMonth() + 1).padStart(2, '0') +
    String(adjustedUserTime.value.getDate()).padStart(2, '0');

  const adjustedUserYesterdayMMDD =
    String(adjustedUserYesterday.value.getMonth() + 1).padStart(2, '0') +
    String(adjustedUserYesterday.value.getDate()).padStart(2, '0');

  // Normalize the holiday list to safe "MMDD" strings
  const holidays = Array.isArray(biz?.holiday)
    ? biz.holiday.map(h => String(h).replace(/\D/g, '').padStart(4, '0'))
    : [];
  const isHoliday = holidays.includes(adjustedUserMMDD);
  const isYesterdayHoliday = holidays.includes(adjustedUserYesterdayMMDD);

  // Yesterday's business hours
  const isOpenFromYesterday = computed(() => {
    // // 🐞 Debug console
    // console.log('Run isOpenFromYesterday')
    for (const r of previousShopBusinessHoursInMinutes.value) {
      // // 🐞 Debug console
      // console.log('r.end: ', r.end)
      // console.log('r.end - 1440: ', r.end - 1440)
      // console.log('adjustedUserTimeInMinutes.value: ', adjustedUserTimeInMinutes.value)
      // console.log('r.end - 1440 - adjustedUserTimeInMinutes.value: ', r.end - 1440 - adjustedUserTimeInMinutes.value)
      if (r.end - 1440 - adjustedUserTimeInMinutes.value > 0) {
        const status = (r.end - 1440 - adjustedUserTimeInMinutes.value < 30) ? 'closeSoon' : 'open';
        return { status, endFormatted: formatTime(r.end) };
      }
    }
    return { status: 'closed' }
  })
  // Today's business hours
  const isOpenToday = computed(() => {
    // // 🐞 Debug console
    // console.log('Run isOpenToday')
    for (const r of shopBusinessHoursInMinutes.value) {
      // // 🐞 Debug console
      // console.log('r.end: ', r.end)
      // console.log('adjustedUserTimeInMinutes.value: ', adjustedUserTimeInMinutes.value)
      // console.log('r.end - adjustedUserTimeInMinutes.value: ', r.end - adjustedUserTimeInMinutes.value)
      const deltaStart = r.start - adjustedUserTimeInMinutes.value;
      const deltaEnd = r.end - adjustedUserTimeInMinutes.value;
      // Before opening window
      if (deltaStart > 30) {
        return { status: 'closed', startFormatted: formatTime(r.start) };
      }
      if (deltaStart > 0 && deltaStart <= 30) {
        return { status: 'openSoon', startFormatted: formatTime(r.start) };
      }

      // During opening window
      if (deltaEnd > 30 && adjustedUserTimeInMinutes.value >= r.start) {
        return { status: 'open', endFormatted: formatTime(r.end) };
      }
      if (deltaEnd > 0 && deltaEnd <= 30 && adjustedUserTimeInMinutes.value >= r.start) {
        return { status: 'closeSoon', endFormatted: formatTime(r.end) };
      }
    }
    return { status: 'closed' };
  })

  // // 🐞 Debug console
  // console.log("userTimezone:", userTimezone);
  // console.log("shopTimezone:", shopTimezone);
  // console.log("userTime:", currentTime.value);
  // console.log("adjustedUserTime:", adjustedUserTime.value);
  // console.log("Days of Week:", daysOfWeek[adjustedUserTime.value.getDay()]);
  // console.log("adjustedUserMMDD:", adjustedUserMMDD);
  // console.log("holidays:", holidays);
  // console.log("isHoliday:", isHoliday);
  // console.log("---END---");


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
  if ((isHoliday && isYesterdayHoliday) || (isHoliday && previousShopBusinessHoursInMinutes.value.length === 0)) {
    onsole.log('Run holiday logic with isClosedFromYesterday')
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

  if (isHoliday && !isYesterdayHoliday && previousShopBusinessHoursInMinutes.value.length > 0) {
    // // 🐞 Debug console
    // console.log('Run holiday logic with isOpenFromYesterday')
    if (isOpenFromYesterday.value.status === 'open') {
      state = 'Open';
      stateClass = 'isOpen';
      nextTime = 'Closes at ' + isOpenFromYesterday.value.endFormatted;
      nextTimeClass = 'isDefault';
      return {
        state,
        stateClass,
        nextTime,
        nextTimeClass,
      };
    } else if (isOpenFromYesterday.value.status === 'closeSoon') {
      state = 'Close Soon';
      stateClass = 'isBetween';
      nextTime = 'Close at ' + isOpenFromYesterday.value.endFormatted;
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
  if (!isHoliday && !isYesterdayHoliday) {
    // // 🐞 Debug console
    // console.log('Run general logic')
    const finish = () => ({
      state,
      stateClass,
      nextTime,
      nextTimeClass,
    });
    if (isOpenFromYesterday.value.status === 'open') {
      state = 'Open';
      stateClass = 'isOpen';
      nextTime = 'Closes at ' + isOpenFromYesterday.value.endFormatted;
      nextTimeClass = 'isDefault';
    } else if (isOpenFromYesterday.value.status === 'closeSoon') {
      state = 'Close Soon';
      stateClass = 'isBetween';
      nextTime = 'Close at ' + isOpenFromYesterday.value.endFormatted;
      nextTimeClass = 'isDefault';
    } else if (isOpenFromYesterday.value.status === 'closed' && isOpenToday.value.status === 'closed') {
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
    } else if (isOpenToday.value.status === 'open') {
      state = 'Open';
      stateClass = 'isOpen';
      nextTime = 'Closes at ' + isOpenToday.value.endFormatted;
      nextTimeClass = 'isDefault';
    } else if (isOpenToday.value.status === 'closeSoon') {
      state = 'Close Soon';
      stateClass = 'isBetween';
      nextTime = 'Close at ' + isOpenToday.value.endFormatted;
      nextTimeClass = 'isDefault';
    } else if (isOpenToday.value.status === 'closed') {
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
    } else if (isOpenToday.value.status === 'openSoon') {
      state = 'Open Soon';
      stateClass = 'isBetween';
      nextTime = 'Opens at ' + isOpenToday.value.startFormatted;
      nextTimeClass = 'isDefault';
    }
    return finish();
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

.list-container {
  align-items: flex-start;
  gap: var(--unit);
  align-self: stretch;
}

.icon {
  min-width: 20px;
  height: 20px;
}
</style>