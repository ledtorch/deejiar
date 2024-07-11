<template>
  <div class="body">
    <div class="frame flex-col">
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

      <footer class="footer">
        <div class="btn-frame">
          <!-- <button>Log out</button> -->
          <div class="button-set">
            <a href="https://twitter.com/deejiar" style="text-decoration: none; color: inherit;">
              <img class="social-button" src="/icon/social/twitter.png" alt="Twitter">
            </a>
            <a href="https://www.instagram.com/deejiar" style="text-decoration: none; color: inherit;">
              <img class="social-button" src="/icon/social/instagram.png" alt="Instagram">
            </a>
          </div>
        </div>
        <p class="caption2">Version 4 (2024.04.30)</p>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
};
</script>

<style lang="scss" scoped>
.body {
  position: relative;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  overflow-y: auto;

  /* Media query for screen widths 430px and below */
  @media (max-width: 430px) {
    padding-bottom: 99px;
  }
}

.frame {
  // width: 100vw;
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
  justify-content: space-between;
  align-items: flex-start;
  align-self: stretch;
  padding-left: 0px;
}

.footer {
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

.social-button {
  width: 24px;
  height: 24px;
}

.button-set {
  align-items: flex-start;
  align-self: stretch;
  gap: 12px;
}
</style>