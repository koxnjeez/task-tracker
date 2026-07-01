<template>
  <div class="unauthenticated centering" v-if="!employeeStore.isAuthenticated">
    <label>Log in to your account</label>
    <router-link to="/auth">Sign in</router-link>
  </div>
  <div class="projects" v-else>
    <button class="button" @click="projectAdding = true">Add project</button>
  </div>
  <modal-project v-if="projectAdding" v-model="projectAdding"></modal-project>
</template>

<script setup>
import { useStoreEmployee } from "@/stores/storeEmployee";
import ModalProject from "@/components/tasks&projects/ModalProject.vue";
import { ref } from "vue";

const employeeStore = useStoreEmployee();
const projectAdding = ref(false);
</script>

<style scoped>
.unauthenticated {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  align-items: center;
}
.unauthenticated a {
  text-decoration: none;
  background: rgba(255, 255, 255, 0.4);
  color: rgba(255, 255, 255, 0.6);
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  font-weight: 900;
}
.button {
  margin: 1.5rem;
}
</style>
