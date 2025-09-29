<template>
  <section class="subscription-section">

    <div class="plans-container">

      <!-- Monthly Plan -->
      <div class="plan-card" :class="{ 'selected': selectedPlan === 'monthly' }" @click="selectedPlan = 'monthly'">
        <div class="monthly-container">
          <div class="plan-header">
            <p class="plan-title _subtitle">Trailblazer Monthly</p>
            <div class="radio-button" :class="{ 'checked': selectedPlan === 'monthly' }">
            </div>
          </div>
          <h5 class="price">$4.99/mo</h5>
        </div>
      </div>

      <Divider />

      <!-- Yearly Plan -->
      <div class="plan-card" :class="{ 'selected': selectedPlan === 'yearly' }" @click="selectedPlan = 'yearly'">
        <div class="yearly-container">
          <div class="yearly-header">
            <div class="plan-header">
              <p class="plan-title _subtitle">Trailblazer Yearly</p>
              <div class="radio-button" :class="{ 'checked': selectedPlan === 'yearly' }">
              </div>
            </div>
            <h5 class="price">$49/yr</h5>
          </div>

          <div class="bonus-container">
            <img class="bonus-icon" src="@/assets/icons/key.png">
            <p class="bonus-text _button-secondary">Join <a class="club-link"
                href="https://x.com/i/communities/1962023966777995432">Deejiar Club</a></p>
          </div>
          <div class="bonus-container">
            <img class="bonus-icon" src="@/assets/icons/discount.png">
            <p class="bonus-text _button-secondary">Save over 20% with the yearly plan</p>
          </div>

        </div>
      </div>
    </div>

    <!-- Terms Text -->
    <p class="_caption1 terms-text">
      Free 7 days, then {{ selectedPlan === 'monthly' ? '$4.99/month' : '$49/year' }}. Renews automatically until
      canceled.
    </p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import Divider from '../common/Divider.vue'

// State
const selectedPlan = ref('yearly') // Default to yearly as shown in the design

// Emit selected plan to parent if needed
const emit = defineEmits(['planSelected'])

// Watch for plan changes
import { watch } from 'vue'
watch(selectedPlan, (newPlan) => {
  emit('planSelected', newPlan)
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
  align-items: center;
}

.bonus-icon {
  width: 24px;
  height: 24px;
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


.terms-text {
  color: var(--tertiary-text);
  padding: 0 var(--box);
  margin-top: auto;
  padding-bottom: var(--block);
  text-align: center;
}
</style>