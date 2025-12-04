<template>
  <section class="subscription-section">
    <div class="main-container">
      <div class="plans-container">

        <!-- Monthly Plan -->
        <div class="plan-card" :class="{ 'selected': selectedId === '$rc_monthly' }"
          @click="$emit('select', '$rc_monthly')">
          <div class="monthly-container">
            <div class="plan-header">
              <p class="plan-title _subtitle">Trailblazer Monthly</p>
              <div class="radio-button" :class="{ 'checked': selectedId === '$rc_monthly' }"></div>
            </div>
            <h5 class="price">{{ monthlyPackage?.product?.priceString }}</h5>
            <div class="bonus-container">
              <img class="bonus-icon" src="@/assets/icons/key.png">
              <p class="bonus-text _button-secondary">
                Join <a class="club-link" href="https://x.com/i/communities/1962023966777995432">Deejiar Club</a>
              </p>
            </div>
          </div>

        </div>

        <Divider />

        <!-- Yearly Plan -->
        <div class="plan-card" :class="{ 'selected': selectedId === '$rc_annual' }"
          @click="$emit('select', '$rc_annual')">
          <div class="yearly-container">
            <div class="yearly-header">
              <div class="plan-header">
                <p class="plan-title _subtitle">Trailblazer Yearly</p>
                <div class="radio-button" :class="{ 'checked': selectedId === '$rc_annual' }"></div>
              </div>
              <h5 class="price">{{ yearlyPackage?.product?.priceString }}</h5>
            </div>

            <div class="bonus-container">
              <img class="bonus-icon" src="@/assets/icons/key.png">
              <p class="bonus-text _button-secondary">
                Join <a class="club-link" href="https://x.com/i/communities/1962023966777995432">Deejiar Club</a>
              </p>
            </div>
            <div class="bonus-container">
              <img class="bonus-icon" src="@/assets/icons/discount.png">
              <p class="bonus-text _button-secondary">Save over 20% with the yearly plan</p>
            </div>
          </div>
        </div>
      </div>
      <p class="_caption1 feature-text">
        <b>Priority Feature Requests</b><br>
        Share what you want to see next—from new stores and cities to fresh feature ideas. Subscribers receive priority
        consideration in shaping future updates.
      </p>
    </div>

    <!-- Terms Text -->
    <p class="_caption1 terms-text">
      By subscribing, you agree to our
      <a href="https://landing.deejiar.com/terms-of-use" class="link-text">Terms of Use Policy</a>
      and
      <a href="https://landing.deejiar.com/privacy-policy" class="link-text">Privacy Policy</a>. First-time subscribers
      receive a 7-day free trial. After the trial, your subscription starts on <b>{{ trialEndDate }}</b> and will renew
      automatically at <b>{{ selectedPriceString }} per {{ selectedPeriod }}</b>. You can cancel anytime in your Apple
      ID account settings.
    </p>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import Divider from '../common/Divider.vue'

const props = defineProps({
  monthlyPackage: Object,
  yearlyPackage: Object,
  selectedId: String
})

defineEmits(['select'])

const trialEndDate = computed(() => {
  const date = new Date()
  date.setDate(date.getDate() + 7)

  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
})

const selectedPriceString = computed(() => {
  if (props.selectedId === '$rc_monthly') {
    return props.monthlyPackage?.product?.priceString
  }
  return props.yearlyPackage?.product?.priceString
})

const selectedPeriod = computed(() => {
  return props.selectedId === '$rc_monthly' ? 'month' : 'year'
})

</script>

<style lang="scss" scoped>
.subscription-section {
  display: flex;
  flex-direction: column;
  gap: var(--division);
  width: 100%;
  height: 100%;
}

.main-container {
  flex-direction: column;
  gap: var(--division);
}

.plans-container {
  flex-direction: column;
  gap: var(--unit);
  border-radius: var(--round-l);
  border: 1px solid var(--tertiary-text);
  padding: var(--division);
  width: 100%;
}

.plan-card {
  /* Layout & Box Model */
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--unit);

  /* Interaction */
  cursor: pointer;
  transition: all 0.2s ease;

  /* Opacity control for unselected plans */
  &:not(.selected) {

    .price,
    .bonus-text,
    .bonus-icon {
      opacity: 0.4;
    }
  }

  /* Full opacity for selected plans */
  &.selected {

    .price,
    .bonus-text,
    .bonus-icon {
      opacity: 1;
    }
  }
}

.monthly-container {
  /* Layout */
  flex-direction: column;
  gap: var(--atom);
  flex: 1;
  padding: var(--box);
  width: 100%;
}

.yearly-container {
  /* Layout */
  flex-direction: column;
  gap: var(--atom);
  flex: 1;
  padding: var(--box);
  width: 100%;
}

.yearly-header {
  flex-direction: column;
}

.bonus-text {
  color: var(--primary-text);
}

.bonus-container {
  gap: var(--atom);
  align-items: start;
}

.bonus-icon {
  width: 20px;
  height: 20px;
}

.plan-title {
  /* Typography */
  color: var(--primary-text);
  width: 100%;

  flex: 1; // Takes available space
  margin: 0; // Reset default margin
}

.plan-header {
  /* Layout */
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}

.price {
  color: var(--primary-text);
}

.period {
  /* Typography */
  font-size: var(--font-2nd);
  font-weight: 400;
  color: var(--secondary-text);
}

.savings {
  /* Typography */
  color: var(--tertiary-text);
  margin: 0;
  margin-top: var(--atom);
}

.savings-highlight {
  /* Typography */
  color: var(--color-green);
  font-weight: 600;
}

.radio-button {
  /* Layout & Box Model */
  width: 16px;
  height: 16px;
  border-radius: 50%;
  margin: 4px;
  border: 2px solid var(--tertiary-text);

  /* Positioning for inner dot */
  display: flex;
  align-items: center;
  justify-content: center;

  /* Interaction */
  transition: all 0.2s ease;

  &.checked {
    // border-color: var(--primary-text);
    border: 5px solid var(--primary-text);
  }
}

@keyframes scaleIn {
  from {
    transform: scale(0);
  }

  to {
    transform: scale(1);
  }
}

.benefits-text {
  /* Typography */
  color: var(--secondary-text);
  margin: 0;
  line-height: 1.5;
}

.club-link {
  /* Typography */
  color: var(--primary-text);
  text-decoration: underline;
  text-decoration-color: var(--tertiary-text);
  text-underline-offset: 2px;
  cursor: pointer;

  &:hover {
    text-decoration-color: var(--primary-text);
  }
}

.feature-text {
  padding: 0 var(--box);
  color: var(--secondary-text);
}

.terms-text {
  color: var(--tertiary-text);
  padding: 0 var(--box);
  margin-top: auto;
  padding-bottom: var(--block);
  // text-align: center;
}

.link-text {
  color: var(--secondary-text);
  text-decoration: underline;
}
</style>