<template>
  <div class="frame">
    <h1>BistroMap</h1>
    <button @click="loginWithTwitter">Login with Twitter</button>
  </div>
</template>
  
<script>
import firebase from "firebase/app";
import "firebase/auth";

export default {
  methods: {
    loginWithTwitter() {
      const provider = new firebase.auth.TwitterAuthProvider();

      firebase
        .auth()
        .signInWithPopup(provider)
        .then((result) => {
          console.log("User signed in with Twitter:", result.user);
        })
        .catch((error) => {
          console.error("Error logging in with Twitter:", error);
        });
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
</style>
