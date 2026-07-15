import { defineStore } from "pinia";
import api from "@/api/api";
import { useStoreProjects } from "./storeProjects";

export const useStoreEmployee = defineStore("storeEmployee", {
  state: () => {
    return {
      user: null,
      token: localStorage.getItem("access_token") || null,
      otherEmployees: [],
      employeesLoaded: false,
      assigned: [],
      unassigned: [],
      assigneesLoaded: false,
    };
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async loginWithGoogle(googleToken) {
      try {
        const response = await api.post("/auth/google", {
          token: googleToken,
        });
        const { access_token } = response.data; // деструктуризация, из response.data вытягивается поле и записывается в точно такое название

        this.token = access_token;
        localStorage.setItem("access_token", access_token);

        await this.fetchCurrentUser();

        return true;
      } catch (error) {
        console.error("Google authentication failed:", error);
        this.logout();
      }
    },
    async fetchCurrentUser() {
      try {
        const response = await api.get("/auth/me");
        this.user = response.data;
      } catch (error) {
        console.error("Failed to fetch a user:", error);
        this.logout();
      }
    },
    logout() {
      try {
        this.token = null;
        this.user = null;
        this.otherEmployees = [];
        this.employeesLoaded = false;
        this.assigned = [];
        this.unassigned = [];
        this.assigneesLoaded = false;
        localStorage.removeItem("access_token");

        const projectsStore = useStoreProjects();
        projectsStore.clearProjects();
      } catch (error) {
        console.error("Logout error:", error);
      }
    },
    async updatePersonalInfo(statement) {
      try {
        const response = await api.patch("/auth/updateinfo", statement);
        this.user = response.data;

        return response.data;
      } catch (error) {
        console.error("Update personal info error:", error);
      }
    },
    async getAllEmployees() {
      try {
        const response = await api.get("/auth/allemployees");
        this.otherEmployees = response.data;

        this.employeesLoaded = true;
        return this.otherEmployees;
      } catch (error) {
        console.error("Failed loading the rest employees:", error);
      }
    },
    async fetchAssigneesData(task_id, project_id) {
      if (this.assigneesLoaded) return;

      try {
        const response = await api.get(
          `/projects/${project_id}/tasks/${task_id}/assignees`,
        );
        this.assigned = response.data.assigned;
        this.unassigned = response.data.unassigned;
        this.assigneesLoaded = true;
      } catch (error) {
        console.error("Failed to fetch assignees data:", error);
        throw error;
      }
    },
  },
});
