<template>
  <div class="body-section">
    <h2>Profile</h2>
    <div class="account-section"></div>
    <div class="splitline"></div>
    <div class="page-card">
      <p>Quick Guide</p>
    </div>
    <div class="page-card">
      <p>Invite your friends</p>
    </div>
    <div class="page-card">
      <p>Taste Book</p>
    </div>
    <div class="page-card">
      <p>Settings</p>
    </div>
    <div class="page-card">
      <p>Contact Us</p>
    </div>
    <div class="page-card">
      <p>Help</p>
    </div>
    <div class="bottom-section">
      <div class="btn-frame">
        <button>Log out</button>
        <div class="btn-set"></div>
      </div>
      <p>Version 1 (2023.08.17)</p>
    </div>
  </div>
</template>
  
<script>
import { useRoute } from "vue-router";
import { useHead } from 'unhead';

export default {
  setup() {
    useHead({
      title: 'Tītsia - Account',
    })
  },
};
</script>
  
<style lang="scss" scoped>
.body-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 24px;
  width: 100%;
  padding: 0px 24px;
}

.account-section {
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}

.btn-frame {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  align-self: stretch;
  padding-left: 0px;
}

.bottom-section {
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  gap: 24px;
  padding: 24px 12px 0px 0px;
}

.btn-set {
  align-items: flex-start;
  gap: 24px;
}

.page-card {
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
  padding: 12px;
}

.splitline {
  justify-content: center;
  align-items: center;
  align-self: stretch;
  width: 100%;
  height: 1px;
  background: var(--4-base-dark-base, rgba(255, 255, 255, 0.07));
}
</style>
  