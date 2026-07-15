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
      this.clearTasks();

      try {
        const response = await api.get(`/projects/${project_id}/tasks`);
        this.tasks = response.data;
        this.tasksLoaded = true;
      } catch (error) {
        console.error("Failed to fetch tasks for current project:", error);
        throw error;
      }
    },
    async createNewTask(project_id, statement) {
      try {
        const response = await api.post(
          `/projects/${project_id}/tasks`,
          statement,
        );
        this.tasks.push(response.data);
        return response.data;
      } catch (error) {
        console.error("Failed task creating:", error);
        throw error;
      }
    },
    async updateTaskInfo(project_id, statement) {
      try {
        const response = await api.patch(
          `/projects/${project_id}/tasks/edittask`,
          statement,
        );
        const updatedTask = response.data;

        const index = this.tasks.findIndex(
          (task) => task.id === updatedTask.id,
        );
        if (index !== -1) {
          this.tasks[index] = updatedTask;
        }
        return updatedTask;
      } catch (error) {
        console.error("Failed task info update:", error);
        throw error;
      }
    },
    clearTasks() {
      this.tasks = [];
      this.tasksLoaded = false;
    },
  },
});
