import axios from "axios";
import { useStoreEmployee } from "@/stores/storeEmployee";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  const employeeStore = useStoreEmployee();
  const token = employeeStore.token;

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
