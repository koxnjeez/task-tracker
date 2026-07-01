<template>
  <div class="auth-container centering">
    <p class="welcome-title">Welcome in Tracky!</p>
    <button-google-auth></button-google-auth>
  </div>
</template>

<script setup>
import ButtonGoogleAuth from "@/components/auth/ButtonGoogleAuth.vue";
</script>

<style scoped>
.welcome-title {
  display: flex;
  justify-content: center;
}
</style>
