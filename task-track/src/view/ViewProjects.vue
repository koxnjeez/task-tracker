<template>
  <div class="unauthenticated centering" v-if="!employeeStore.isAuthenticated">
    <label>Log in to your account</label>
    <router-link to="/auth">Sign in</router-link>
  </div>
  <div class="projects" v-else>
    <button class="button" @click="openCreateModal">Add project</button>
    <div class="headers-section">
      <div class="id-header">INDEX</div>
      <div class="title-header">TITLE</div>
      <div class="privacy-header">PRIVACY</div>
    </div>
    <ul>
      <project
        v-for="project in projectsStore.projects"
        :key="project.id"
        :project="project"
        @updateProject="openEditModal(project)"
      ></project>
    </ul>
  </div>
  <modal-project
    v-if="openModal"
    v-model="openModal"
    :editingProject="selectedProject"
  ></modal-project>
</template>

<script setup>
import { useStoreEmployee } from "@/stores/storeEmployee";
import { useStoreProjects } from "@/stores/storeProjects";
import ModalProject from "@/components/tasks&projects/ModalProject.vue";
import Project from "@/components/tasks&projects/Project.vue";
import { ref, onMounted } from "vue";

const employeeStore = useStoreEmployee();
const projectsStore = useStoreProjects();
const openModal = ref(false);
const selectedProject = ref(null);

onMounted(async () => {
  await projectsStore.fetchProjects();
});

const openCreateModal = () => {
  selectedProject.value = null;
  openModal.value = true;
};

const openEditModal = (project) => {
  selectedProject.value = project;
  openModal.value = true;
};
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
.headers-section {
  display: flex;
  padding: 1.5rem;
  font-weight: 900;
  border-bottom: 1px solid rgba(255, 255, 255, 0.7);
}
.id-header {
  width: 10%;
}
.title-header {
  width: 75%;
}
.privacy-header {
  width: 15%;
}
ul {
  padding: 0;
  margin: 0;
}
</style>
