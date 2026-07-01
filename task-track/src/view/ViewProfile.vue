<template>
  <div class="profile-container centering">
    <div class="profile-title">Personal info</div>
    <ul>
      <li>
        Full name: {{ employeeStore.user.last_name }}
        {{ employeeStore.user.first_name }} {{ employeeStore.user.middle_name }}
      </li>
      <li>Email: {{ employeeStore.user.email }}</li>
      <li>
        Phone number:
        {{
          employeeStore.user.phone_number
            ? employeeStore.user.phone_number
            : "—"
        }}
      </li>
    </ul>
    <div class="buttons-container">
      <button class="button" @click="dataEditing = true">Update info</button>
      <button class="button button-dark" @click="logout">Log out</button>
    </div>
    <modal-profile-data v-model="dataEditing"></modal-profile-data>
  </div>
</template>

<script setup>
import ModalProfileData from "@/components/auth/ModalProfileData.vue";
import { useStoreEmployee } from "@/stores/storeEmployee";
import router from "@/router";
import { ref } from "vue";

const employeeStore = useStoreEmployee();

const logout = () => {
  employeeStore.logout();
  router.push("/auth");
};

const dataEditing = ref(false);
</script>

<style scoped>
.profile-title {
  font-size: 30px;
  font-weight: 600;
  justify-self: center;
  margin-bottom: 2rem;
}
.profile-container {
  background: rgba(255, 255, 255, 0.2);
  width: 50%;
  max-width: 38rem;
  backdrop-filter: blur(20px);
  padding: 1rem;
  border-radius: 10px;
}
ul {
  padding: 0;
  margin: 0.2rem 0;
  list-style: none;
}
.buttons-container {
  margin-top: 1rem;
  display: flex;
  gap: 1rem;
}
</style>
