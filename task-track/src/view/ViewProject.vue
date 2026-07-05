<template>
  <div class="project-container">
    <button class="button" @click="assignManagement = true">
      Employee Assignment Management
    </button>
  </div>
  <modal-employee-assigning
    v-if="assignManagement"
    v-model="assignManagement"
  ></modal-employee-assigning>
</template>

<script setup>
import ModalEmployeeAssigning from "@/components/tasks&projects/ModalEmployeeAssigning.vue";
import { ref } from "vue";

const assignManagement = ref(false);
</script>

<style scoped>
.button {
  width: 100%;
  margin-top: 1.5rem;
}
</style>
