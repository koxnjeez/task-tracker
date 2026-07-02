import { defineStore } from "pinia";
import api from "@/api/api";

export const useStoreProjects = defineStore("storeProjects", {
  state: () => {
    return {
      projects: [],
      isLoaded: false,
    };
  },
  actions: {
    async createNewProject(statement) {
      try {
        const response = await api.post("/projects/newproject", statement);
        this.projects.push(response.data);
        return response.data;
      } catch (error) {
        console.error("Failed project creating:", error);
        throw error;
      }
    },
    async updateProjectInfo(statement) {
      try {
        const response = api.patch("/projects/editproject", statement);
        const updatedProject = response.data;

        const index = this.projects.findIndex(
          (p) => p.id === updatedProject.id,
        );
        if (index !== -1) {
          this.projects[index] = updatedProject;
        }
        return updatedProject;
      } catch (error) {
        console.error("Failed project info update:", error);
        throw error;
      }
    },
    async fetchProjects() {
      if (this.isLoaded) return;

      try {
        const response = await api.get("/projects");
        this.projects = response.data;
        this.isLoaded = true;
      } catch (error) {
        console.error("Failed to fatch available projects:", error);
        throw error;
      }
    },
    clearProjects() {
      this.projects = [];
      this.isLoaded = false;
    },
  },
});
