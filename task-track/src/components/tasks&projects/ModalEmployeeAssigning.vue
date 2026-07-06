<template>
  <teleport to="body">
    <div class="modal-background" @click="closeModal"></div>
    <dialog open>
      <div class="assigning-container">
        <div class="employees-container">
          <ul class="employees-list">
            <li
              v-for="employee in employeeStore.otherEmployees"
              :key="employee.id"
              class="employee-item"
            >
              {{ employee.last_name }}
              {{ employee.first_name }}
              {{ employee.middle_name }}
              <br />{{ employee.phone_number }}
            </li>
          </ul>
        </div>
        <div class="roles-container">
          <div class="role" v-for="role in projectsStore.roles" :key="role.id">
            <label class="switch">
              <input type="checkbox" />
              <span class="slider"></span>
            </label>
            <label class="role-title">{{ role.name }}</label>
          </div>
        </div>
      </div>
    </dialog>
  </teleport>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useStoreEmployee } from "@/stores/storeEmployee";
import { useStoreProjects } from "@/stores/storeProjects";
import api from "@/api/api";

// data
const employeeStore = useStoreEmployee();
const projectsStore = useStoreProjects();
const route = useRoute();
const selectedRolesMap = ref({});
const selectedEmployeeId = ref(null);

// props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
});

// emits
const emit = defineEmits(["update:modelValue"]);

// alternative close
const handleKeybord = (e) => {
  if (e.key === "Escape") {
    closeModal();
  }
};

// modal close
const closeModal = () => {
  selectedRolesMap.value = {};
  selectedEmployeeId.value = null;
  emit("update:modelValue", false);
};

// load when mount
onMounted(async () => {
  document.addEventListener("keyup", handleKeybord);

  if (!employeeStore.employeesLoaded) {
    await employeeStore.getAllEmployees();
  }
  await projectsStore.getAllRoles();

  employeeStore.otherEmployees.forEach((employee) => {
    selectedRolesMap.value[employee.id] = [];
  });

  try {
    const response = await api.get(
      `/projects/${parseInt(route.params.id)}/members`,
    );
    const activeMembers = response.data;

    activeMembers.forEach((member) => {
      if (selectedRolesMap.value[member.employee_id]) {
        selectedRolesMap.value[member.employee_id].push(member.role_id);
      }
    });
  } catch (error) {
    console.error("Failed to load project members data:", error);
  }

  if (employeeStore.otherEmployees.length > 0) {
    selectedEmployeeId.value = employeeStore.otherEmployees.id;
  }
});

onUnmounted(() => {
  document.removeEventListener("keyup", handleKeybord);
});

const refreshProjectRoles = async () => {
  const payload = [];

  Object.keys(selectedRolesMap.value).forEach((employeeId) => {
    const activeRoles = selectedRolesMap.value[employeeId];

    activeRoles.forEach((roleId) => {
      payload.push({
        employee_id: parseInt(employeeId),
        role_id: roleId,
      });
    });
  });

  try {
    await api.post(`/projects/${parseInt(route.params.id)}/members`);
    alert("Roles saved successfully!");
  } catch (error) {
    console.error("Failed saving roles settings");
  }
};
</script>

<style scoped>
dialog {
  width: 50%;
  /* проставить мин/макс ширину */
}
.assigning-container {
  width: 100%;
  height: 100%;
  display: flex;
}
.employees-container {
  background: rgba(255, 255, 255, 0.3);
  height: 25rem;
  width: 60%;
  border-radius: 10px;
}
.employees-list {
  padding: 1rem;
  margin: 0;
}
.employee-item {
  list-style: none;
  background: rgba(0, 0, 0, 0.6);
  margin-bottom: 0.3rem;
  padding: 0.5rem 0.7rem;
  border-radius: 10px;
  border: none;
  box-shadow: 0 4px 8px rgba(27, 27, 27, 0.3);
}
.employee-item:last-child {
  margin-bottom: 0;
}
.roles-container {
  height: fit-content;
  width: 40%;
  padding: 0.5rem 1rem;
}
.role {
  display: flex;
  margin-bottom: 1rem;
}
.role-title {
  text-transform: capitalize;
  align-content: center;
  margin-left: 0.5rem;
}
</style>
