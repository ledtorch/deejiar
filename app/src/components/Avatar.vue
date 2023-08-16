<template>
  <div class="frame">
    <h1>BistroMap</h1>
    <button
      class="icon-button"
      @click="loginWithTwitter"
      :class="buttonClass"
      :style="buttonStyle"
    ></button>
  </div>
</template>
  
<script>
// import firebase from "firebase/app";
// import "firebase/auth";

export default {
  // methods: {
  //   loginWithTwitter() {
  //     const provider = new firebase.auth.TwitterAuthProvider();
  //     firebase
  //       .auth()
  //       .signInWithPopup(provider)
  //       .then((result) => {
  //         console.log("User signed in with Twitter:", result.user);
  //       })
  //       .catch((error) => {
  //         console.error("Error logging in with Twitter:", error);
  //       });
  //   },
  // },
  computed: {
    buttonStyle() {
      return {
        backgroundImage: "url('/Icon/Avatar.png')",
      };
    },
  },
};
</script>
  
<style>
.frame {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: flex-start;
}

.icon-button {
  background: no-repeat center/contain;
  width: 36px;
  height: 36px;
  border: none;
  cursor: pointer;
  padding: 0;
  transition: transform 0.2s ease;
}
</style>
