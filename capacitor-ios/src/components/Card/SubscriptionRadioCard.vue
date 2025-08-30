<template>
  <section class="subscription-section">

    <div class="plans-container">

      <!-- Monthly Plan -->
      <div class="plan-card" :class="{ 'selected': selectedPlan === 'monthly' }" @click="selectedPlan = 'monthly'">
        <div class="plan-content">
          <div class="plan-header">
            <p class="plan-title _subtitle">Trailblazer Monthly</p>
            <div class="radio-button" :class="{ 'checked': selectedPlan === 'monthly' }">
            </div>
          </div>
          <span class="_title price">$4.99/mo</span>
        </div>


      </div>

      <div class="_divider-horizontal" />

      <!-- Yearly Plan -->
      <div class="plan-card" :class="{ 'selected': selectedPlan === 'yearly' }" @click="selectedPlan = 'yearly'">
        <div class="plan-content">

          <div class="plan-header">
            <p class="plan-title _subtitle">Trailblazer Yearly</p>
            <div class="radio-button" :class="{ 'checked': selectedPlan === 'yearly' }">
            </div>
          </div>


          <span class="_title price">$49/yr</span>
          <p class="_footnote savings">
            Save over <span class="_footnote savings-highlight">20%</span> with the yearly plan.
          </p>




        </div>
      </div>
    </div>

    <!-- Benefits Text -->
    <div class="note">
      <p class="_body2 benefits-text">
        Thank you for being an early supporter. Your subscription unlocks special access to the
        <span class="club-link">Deejiar Club</span>.
      </p>

      <!-- Terms Text -->
      <p class="_caption1 terms-text">
        Free for 7 days, then {{ selectedPlan === 'monthly' ? '$4.99/month' : '$49/year' }}.
        Auto-renews until canceled in Settings.
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

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
  padding: var(--box) 0;
  gap: var(--unit);

  /* Interaction */
  cursor: pointer;
  transition: all 0.2s ease;

  &:active {
    transform: scale(0.98);
  }
}

.plan-content {
  /* Layout */
  display: flex;
  flex-direction: column;
  gap: var(--unit);
  flex: 1;
  width: 100%;
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
  color: var(--tertiary-text);
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
  /* Typography */
  color: var(--tertiary-text);
  margin: 0;
  line-height: 1.4;
}

.note {
  flex-direction: column;
  width: 100%;
  padding: 0 var(--box);
  gap: var(--box);
}

/* Responsive adjustments for smaller screens */
@media (max-width: 390px) {
  .subscription-section {
    padding: 0 var(--division);
  }

  .plan-card {
    padding: var(--division);
  }
}
</style>