import { defineStore } from "pinia";
import api from "@/api/api";

export const useStoreStatuses = defineStore("storeStatuses", {
  state: () => {
    return {
      statuses: [],
      statusesLoaded: false,
    };
  },
  actions: {
    async fetchStatuses(project_id) {
      this.clearStatuses();

      try {
        const response = await api.get(`/projects/${project_id}/statuses`);
        this.statuses = response.data;
        this.statusesLoaded = true;
      } catch (error) {
        console.error("Failed to fetch statuses for current project:", error);
        throw error;
      }
    },
    async createNewStatus(project_id, statement) {
      try {
        const response = await api.post(
          `/projects/${project_id}/statuses`,
          statement,
        );
        this.statuses.push(response.data);
        return response.data;
      } catch (error) {
        console.error("Failed status creating:", error);
        throw error;
      }
    },
    async deleteStatus(project_id, status_id) {
      try {
        await api.delete(`/projects/${project_id}/statuses/${status_id}`);
        this.statuses = this.statuses.filter(
          (status) => status.id !== status_id,
        );
      } catch (error) {
        console.error("Failed status deleting:", error);
        throw error;
      }
    },
    clearStatuses() {
      this.statuses = [];
      this.statusesLoaded = false;
    },
  },
});
