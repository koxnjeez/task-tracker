<template>
  <div class="project-container">
    <div class="buttons-container">
      <button class="button" @click="openCreateModal">Add new task</button>
      <button class="button" @click="assignManagement = true">
        Employee Assignment Management
      </button>
    </div>
    <ul>
      <task v-for="task in tasksStore.tasks" :key="task.id"></task>
    </ul>
  </div>
  <modal-task
    v-if="openModal"
    v-model="openModal"
    :editingTask="selectedTask"
  ></modal-task>
  <modal-employee-assigning
    v-if="assignManagement"
    v-model="assignManagement"
  ></modal-employee-assigning>
</template>

<script setup>
import ModalTask from "@/components/tasks&projects/ModalTask.vue";
import ModalEmployeeAssigning from "@/components/tasks&projects/ModalEmployeeAssigning.vue";
import Task from "@/components/tasks&projects/Task.vue";
import { useStoreTasks } from "@/stores/storeTasks";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const tasksStore = useStoreTasks();
const assignManagement = ref(false);
const openModal = ref(false);
const selectedTask = ref(null);
const projectId = parseInt(route.params.id);

onMounted(async () => {
  await tasksStore.fetchTasks(projectId);
});

const openCreateModal = () => {
  selectedTask.value = null;
  openModal.value = true;
};
const openEditModal = (task) => {
  selectedTask.value = task;
  openModal.value = true;
};
</script>

<style scoped>
.buttons-container {
  display: flex;
  gap: 2rem;
}
.button {
  width: 50%;
  margin-top: 1.5rem;
}
</style>
