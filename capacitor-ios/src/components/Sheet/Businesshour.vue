<template>
  <div>
    <template v-if="viewMode === 'overview'">
      <div>
        <p :class="['subhead', bizHr.stateClass]">{{ bizHr.state }}</p>
        <p class="_color-secondary subhead" v-if="bizHr.isTime">&nbsp;·&nbsp;{{ bizHr.time }}</p>
        <p :class="['subhead', bizHr.nextTimeClass]" v-if="bizHr.isNextTime">&nbsp;·&nbsp;{{ bizHr.nextTime }}</p>
      </div>
    </template>
    <template v-if="viewMode === 'detail'">
      <div class="frame">
        <div class="icon"></div>
        <p :class="['subhead', bizHr.stateClass]">{{ bizHr.state }}</p>
        <p class="_color-secondary subhead" v-if="bizHr.isTime">&nbsp;·&nbsp;{{ bizHr.time }}</p>
        <p :class="['subhead', bizHr.nextTimeClass]" v-if="bizHr.isNextTime">&nbsp;·&nbsp;{{ bizHr.nextTime }}</p>
        <p class="subhead font-semibold">{{ bizHr.currentDayName }}</p>
        <p class="subhead">{{ bizHr.formattedBusinessHours }}</p>
      </div>
    </template>
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

// User's timezone
const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

// Derived user time values
const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const currentDayName = computed(() => daysOfWeek[currentTime.value.getDay()]);
const currentTimeInMinutes = computed(() => currentTime.value.getHours() * 60 + currentTime.value.getMinutes());

// DST-safe offset calculation
function getOffsetMinutesForZone(tz, at = new Date()) {
  const fmt = new Intl.DateTimeFormat('en-US', {
    timeZone: tz,
    hour12: false,
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit'
  });
  const parts = Object.fromEntries(fmt.formatToParts(at).map(p => [p.type, p.value]));
  const asUTC = Date.UTC(+parts.year, +parts.month - 1, +parts.day, +parts.hour, +parts.minute);
  return Math.round((asUTC - at.getTime()) / 60000);
}

function timezoneGapMinutes(userTz, shopTz, at = new Date()) {
  return getOffsetMinutesForZone(shopTz, at) - getOffsetMinutesForZone(userTz, at);
}

// Get local day name, time in minutes, and MMDD in a specific timezone
function getLocalDayName(tz, at) {
  return new Intl.DateTimeFormat('en-US', { timeZone: tz, weekday: 'long' }).format(at);
}

function getLocalTimeInMinutes(tz, at) {
  const fmt = new Intl.DateTimeFormat('en-US', {
    timeZone: tz,
    hour12: false,
    hour: '2-digit',
    minute: '2-digit'
  });
  const parts = fmt.formatToParts(at).reduce((acc, p) => ({ ...acc, [p.type]: p.value }), {});
  return Number(parts.hour) * 60 + Number(parts.minute);
}

function getLocalMMDD(tz, at) {
  const fmt = new Intl.DateTimeFormat('en-US', { timeZone: tz, month: '2-digit', day: '2-digit' });
  const parts = fmt.formatToParts(at);
  const mm = parts.find(p => p.type === 'month').value;
  const dd = parts.find(p => p.type === 'day').value;
  return `${mm}${dd}`;
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

// Collect ranges for a specific day name
function collectRangesForDay(biz, dayName) {
  const raw = biz?.hours?.[dayName] || [];
  return raw
    .filter(r => r && r.start && r.end)
    .map(r => {
      let start = parseHHmm(r.start);
      let end = parseHHmm(r.end);
      if (end <= start) end += 1440;
      return { start, end };
    })
    .sort((a, b) => a.start - b.start);
}

const bizHr = computed(() => {
  const biz = props.bizTime || {};
  const shopTimezone = biz.timezone || 'UTC';

  // Timezone offset (shop - user)
  const tzOffset = timezoneGapMinutes(userTimezone.value, shopTimezone, currentTime.value);

  // Shop-local values for logic
  const shopDayName = getLocalDayName(shopTimezone, currentTime.value);
  const shopTimeInMinutes = getLocalTimeInMinutes(shopTimezone, currentTime.value);
  const shopMMDD = getLocalMMDD(shopTimezone, currentTime.value);

  // Next/prev day for shop
  const nextDayAt = new Date(currentTime.value.getTime() + 86400000);
  const prevDayAt = new Date(currentTime.value.getTime() - 86400000);
  const nextShopDayName = getLocalDayName(shopTimezone, nextDayAt);
  const prevShopDayName = getLocalDayName(shopTimezone, prevDayAt);

  // UI defaults
  let state = '';
  let time = '';
  let isTime = false;
  let nextTime = '';
  let isNextTime = false;
  let stateClass = '';
  let nextTimeClass = '';
  let formattedBusinessHours = '';

  // 1) 24H short-circuit
  const isHoliday = Array.isArray(biz?.holiday) && biz.holiday.includes(shopMMDD);
  if (biz?.['24hr'] === true) {
    state = isHoliday ? 'Closed for Holiday' : 'Open 24H';
    stateClass = isHoliday ? 'isHoliday' : 'isOpen';
    return { state, time, isTime, nextTime, isNextTime, stateClass, nextTimeClass, currentDayName: currentDayName.value, formattedBusinessHours };
  }

  // 2) Holiday
  if (isHoliday) {
    state = 'Closed for Holiday';
    stateClass = 'isHoliday';
    return { state, time, isTime, nextTime, isNextTime, stateClass, nextTimeClass, currentDayName: currentDayName.value, formattedBusinessHours };
  }

  // 3) Regular schedule
  const todayRanges = collectRangesForDay(biz, shopDayName);
  const nextDayRanges = collectRangesForDay(biz, nextShopDayName);

  // Adjust today's ranges to user time for display
  const adjustedRanges = todayRanges.map(r => ({
    start: ((r.start - tzOffset) % 1440 + 1440) % 1440,
    end: ((r.end - tzOffset) % 1440 + 1440) % 1440
  }));
  formattedBusinessHours = adjustedRanges.map(r => `${formatTime(r.start)}–${formatTime(r.end)}`).join(', ') || 'Closed';

  // Check open now (in shop time)
  let openNow = false;
  let closingTime = null; // shop local
  for (const r of todayRanges) {
    if (shopTimeInMinutes >= r.start && shopTimeInMinutes < r.end) {
      openNow = true;
      closingTime = r.end;
      break;
    }
  }

  // Spillover from prev day
  if (!openNow) {
    const prevRanges = collectRangesForDay(biz, prevShopDayName);
    for (const r of prevRanges) {
      if (r.end > 1440 && shopTimeInMinutes < (r.end - 1440)) {
        openNow = true;
        closingTime = r.end - 1440;
        break;
      }
    }
  }

  if (openNow && closingTime !== null) {
    const adjustedClosingTime = ((closingTime - tzOffset) % 1440 + 1440) % 1440;
    const minutesToClose = (adjustedClosingTime - currentTimeInMinutes.value + 1440) % 1440;
    if (minutesToClose < 30) {
      state = `Closes at ${formatTime(adjustedClosingTime)}`;
      stateClass = 'isOpen';
    } else {
      state = 'Open';
      time = `Closes at ${formatTime(adjustedClosingTime)}`;
      isTime = true;
      stateClass = 'isOpen';
    }
  } else {
    // Next open today?
    let foundToday = false;
    for (const r of todayRanges) {
      if (shopTimeInMinutes < r.start) {
        const adjustedStart = ((r.start - tzOffset) % 1440 + 1440) % 1440;
        const minutesToOpen = (r.start - shopTimeInMinutes + 1440) % 1440;
        if (minutesToOpen <= 30) {
          state = 'Opens soon';
          nextTime = `Opens at ${formatTime(adjustedStart)}`;
          isNextTime = true;
          stateClass = 'isClose';
          nextTimeClass = 'isOpen';
        } else {
          state = `Opens at ${formatTime(adjustedStart)}`;
          stateClass = 'isClose';
        }
        foundToday = true;
        break;
      }
    }

    if (!foundToday) {
      // Earliest next day
      let earliestShop = Infinity;
      for (const r of nextDayRanges) earliestShop = Math.min(earliestShop, r.start);
      if (earliestShop !== Infinity) {
        const adjustedEarliest = ((earliestShop - tzOffset) % 1440 + 1440) % 1440;
        state = 'Closed';
        let dayLabel = '';
        if (adjustedEarliest < currentTimeInMinutes.value) {
          dayLabel = 'tomorrow';
        }
        nextTime = `Opens at ${formatTime(adjustedEarliest)}${dayLabel ? ` ${dayLabel}` : ''}`;
        isNextTime = true;
        stateClass = 'isClose';
        nextTimeClass = 'isOpen';
      } else {
        state = 'Closed';
        stateClass = 'isClose';
      }
    }
  }

  return { state, time, isTime, nextTime, isNextTime, stateClass, nextTimeClass, currentDayName: currentDayName.value, formattedBusinessHours };
});
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