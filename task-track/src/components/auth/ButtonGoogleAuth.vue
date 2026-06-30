<template>
  <div class="google-button-container">
    <div ref="googleBtn"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useStoreEmployee } from "@/stores/storeEmployee";
import { useRouter } from "vue-router";

const googleBtn = ref(null);
const employeeStore = useStoreEmployee();
const router = useRouter();

const handleCredentialResponse = async (response) => {
  try {
    const success = await employeeStore.loginWithGoogle(response.credential);

    if (success) {
      router.push("/");
    }
  } catch (error) {
    alert("Google authentication failed, try again.");
  }
};

// рендер кнопки
onMounted(() => {
  /* global google */
  if (typeof google !== "undefined") {
    google.accounts.id.initialize({
      client_id:
        "14911123036-1rubt0p5ppdsss0ibk603094lm1of44f.apps.googleusercontent.com",
      callback: handleCredentialResponse,
    });

    google.accounts.id.renderButton(googleBtn.value, {
      theme: "filled_black",
      size: "large",
      text: "continue_with",
      shape: "pill",
    });
  } else {
    console.error("Google service scripts failed to load.");
  }
});
</script>

<style scoped>
.google-button-container {
  display: flex;
  justify-content: center;
}
</style>
