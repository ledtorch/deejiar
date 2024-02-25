<template>
  <div class="body">
    <div class="body-section">
      <h2 class="strech-attri">Profile</h2>
      <!-- <div class="account-section"></div> -->
      <div class="splitline"></div>
      <!-- <div class="page-card">
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
      </div> -->
      <a href="https://twitter.com/naivebara" class="button">Author</a>
      <a href="https://x.com/deejiar" class="button">X</a>
      <a href="https://instagram.com/deejiar" class="button">Instagram</a>
      <p>Version 2 (2024.02.25)</p>

      <div class="bottom-section">
        <!-- <div class="btn-frame">
          <button>Log out</button>
          <div class="btn-set"></div>
        </div> -->
        <!-- <p>Version 2 (2024.02.25)</p> -->
      </div>
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
.body {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  overflow-y: auto;

  /* Media query for screen widths 430px and below */
  @media (max-width: 430px) {
    padding-bottom: 99px;
  }
}

.body-section {
  // width: 100vw;
  display: flex;
  flex-direction: column;
  align-items: center;
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

// Fonts
.strech-attri {
  width: 100%;
}
</style>
  