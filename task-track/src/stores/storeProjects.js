import { defineStore } from "pinia";
import api from "@/api/api";

export const useStoreProjects = defineStore("storeProjects", {
  state: () => {
    return {
      projects: [],
    };
  },
  actions: {
    async createNewProject(statement) {
      try {
        const response = await api.post("/projects/new-project", statement);
        this.projects.push(response.data);
        return response.data;
      } catch (error) {
        console.error("Failed project creating:", error);
        throw error;
      }
    },
  },
});
