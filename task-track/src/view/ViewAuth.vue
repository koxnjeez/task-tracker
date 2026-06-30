<template>
  <div class="auth-container">
    <p class="welcome-title">Welcome in Tracky!</p>
    <button-google-auth></button-google-auth>
  </div>
</template>

<script setup>
import ButtonGoogleAuth from "@/components/auth/ButtonGoogleAuth.vue";
</script>

<style scoped>
.auth-container {
  position: absolute;
  left: 50%;
  top: calc(50% - (1.75rem));
  /* transform: translate(-50%, -50%); */
  translate: -50% -50%;
}
.welcome-title {
  display: flex;
  justify-content: center;
}
</style>
