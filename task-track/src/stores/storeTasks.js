import { defineStore } from "pinia";
import api from "@/api/api";

export const useStoreTasks = defineStore("storeTasks", {
  state: () => {
    return {
      tasks: [],
      tasksLoaded: false,
    };
  },
  actions: {
    async fetchTasks(project_id) {
      if (this.tasksLoaded) return;

      try {
        const response = await api.get(`/projects/${project_id}/tasks`);
        this.tasks = response.data;
        this.tasksLoaded = true;
      } catch (error) {
        console.error("Failed to fetch tasks for current project:", error);
        throw error;
      }
    },
  },
});
