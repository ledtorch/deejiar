<template>
  <div class="frame">
    <h1>Deejiar</h1>
    <button class="icon-button" @click="loginWithTwitter" :style="buttonStyle"></button>
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
  
<style lang="scss" scoped>
.frame {
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
}

.icon-button {
  cursor: pointer;
  width: 36px;
  height: 36px;
  border: none;
  padding: 0;
  background: no-repeat center/contain;
  transition: transform 0.2s ease;
}
</style>
