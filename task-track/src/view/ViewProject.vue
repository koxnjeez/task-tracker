<template>
  <div class="project-container">
    <h1>{{ projectTitle }}</h1>
    <div class="buttons-container">
      <button class="button" @click="openCreateModal">Add new task</button>
      <button class="button" @click="statusesManagement = true">
        Statuses Management
      </button>
      <button class="button" @click="projectMemberManagement = true">
        Employee Assignment Management
      </button>
    </div>
    <div class="headers-section">
      <div class="id-header">ID</div>
      <div class="title-header">TITLE</div>
      <div class="description-header">DESCRIPTION</div>
      <div class="status-header">STATUS</div>
      <div class="date-header">START DATE</div>
      <div class="date-header">END DATE</div>
      <div class="pull-request-header">PULL REQUEST</div>
    </div>
    <ul>
      <task
        v-for="task in tasksStore.tasks"
        :key="task.id"
        :task="task"
        @click="openEditModal(task)"
        @openTaskAssigning="openAssignmentManagment(task.id)"
      ></task>
    </ul>
  </div>
  <modal-task
    v-if="openModal"
    v-model="openModal"
    :editingTask="selectedTask"
  ></modal-task>
  <modal-statuses
    v-if="statusesManagement"
    v-model="statusesManagement"
  ></modal-statuses>
  <modal-project-members
    v-if="projectMemberManagement"
    v-model="projectMemberManagement"
  ></modal-project-members>
  <modal-assignees
    v-if="assignmentManagement"
    v-model="assignmentManagement"
    :taskId="taskId"
  ></modal-assignees>
</template>

<script setup>
import ModalTask from "@/components/tasks&projects/ModalTask.vue";
import ModalProjectMembers from "@/components/tasks&projects/ModalProjectMembers.vue";
import ModalStatuses from "@/components/tasks&projects/ModalStatuses.vue";
import ModalAssignees from "@/components/tasks&projects/ModalAssignees.vue";
import Task from "@/components/tasks&projects/Task.vue";
import { useStoreTasks } from "@/stores/storeTasks";
import { useStoreProjects } from "@/stores/storeProjects";
import { useStoreStatuses } from "@/stores/storeStatuses";
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";

// data
const route = useRoute();
const tasksStore = useStoreTasks();
const projectsStore = useStoreProjects();
const statusesStore = useStoreStatuses();
const projectMemberManagement = ref(false);
const openModal = ref(false);
const selectedTask = ref(null);
const statusesManagement = ref(false);
const assignmentManagement = ref(false);
const projectId = parseInt(route.params.id);
const taskId = ref(null);

// load when mount
onMounted(async () => {
  await tasksStore.fetchTasks(projectId);
  await statusesStore.fetchStatuses(projectId);

  if (projectsStore.projects.length === 0) {
    try {
      await projectsStore.fetchProjects();
    } catch (error) {
      console.error("Failed to fetch the project:", error);
      throw error;
    }
  }
});

// modal variaties
const openCreateModal = () => {
  selectedTask.value = null;
  openModal.value = true;
};
const openEditModal = (task) => {
  selectedTask.value = task;
  openModal.value = true;
};

// computed
const projectTitle = computed(() => {
  const project = projectsStore.projects.find(
    (project) => project.id === projectId,
  );

  return project?.title || "Loading...";
});

const openAssignmentManagment = (task_id) => {
  taskId.value = task_id;
  assignmentManagement.value = true;
};
</script>

<style scoped>
.buttons-container {
  display: flex;
  gap: 2rem;
}
.button {
  width: 50%;
}
ul {
  margin: 0;
  padding: 0;
}
h1 {
  margin: 0;
  padding: 2rem;
  justify-self: center;
  font-size: 40px;
  font-weight: 900;
}
.headers-section {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  padding-right: 4.5rem;
  margin-top: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.7);
}
.id-header {
  width: 3%;
}
.title-header {
  width: 20%;
}
.description-header {
  width: 30%;
}
.status-header {
  width: 12%;
}
.date-header {
  width: 10%;
}
.pull-request-header {
  width: 15%;
}
</style>
