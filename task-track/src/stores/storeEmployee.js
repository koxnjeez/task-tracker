import { defineStore } from "pinia";
import api from "@/api/api";

export const useStoreEmployee = defineStore("storeEmployee", {
  state: () => {
    return {
      user: null,
      token: localStorage.getItem("access_token") || null,
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
        console.error("Failed to fetch:", error);
        this.logout();
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("access_token");
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
  },
});
