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
              :class="{
                'selected-employee': employee.id == selectedEmployeeId,
                'project-member': selectedRolesMap[employee.id]?.length > 0,
              }"
              @click="selectedEmployeeId = employee.id"
            >
              {{ employee.last_name }}
              {{ employee.first_name }}
              {{ employee.middle_name }}
              <br />{{ employee.phone_number }}
            </li>
          </ul>
        </div>
        <div
          class="roles-container"
          v-if="selectedEmployeeId && selectedRolesMap[selectedEmployeeId]"
        >
          <div class="role" v-for="role in projectsStore.roles" :key="role.id">
            <label class="switch">
              <input
                type="checkbox"
                :value="role.id"
                v-model="selectedRolesMap[selectedEmployeeId]"
              />
              <span class="slider"></span>
            </label>
            <label class="role-title">{{ role.name }}</label>
          </div>
          <button class="button button-dark" @click="refreshProjectRoles">
            Save changes
          </button>
        </div>
      </div>
    </dialog>
  </teleport>
</template>

<script setup>
import { onMounted, onUnmounted, ref, watch } from "vue";
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
const projectId = parseInt(route.params.id);

// props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
});

// emits
const emit = defineEmits(["update:modelValue"]);

// watch
watch(
  () => employeeStore.otherEmployees,
  (newEmployees) => {
    if (newEmployees.length > 0 && !selectedEmployeeId.value) {
      selectedEmployeeId.value = newEmployees[0].id;
    }
  },
  { immediate: true },
);

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
    const response = await api.get(`/projects/${projectId}/members`);
    const activeMembers = response.data;

    activeMembers.forEach((member) => {
      if (selectedRolesMap.value[member.employee_id]) {
        selectedRolesMap.value[member.employee_id].push(member.role_id);
      }
    });
  } catch (error) {
    console.error("Failed to load project members data:", error);
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

  console.log("Sends on backend:", JSON.stringify(payload));

  try {
    await api.post(`/projects/${projectId}/members`, payload);
    alert("Roles saved successfully!");
    closeModal();
  } catch (error) {
    console.error("Failed saving roles settings:", error);
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
  box-sizing: content-box;
  background: rgba(0, 0, 0, 0.6);
  margin-bottom: 0.3rem;
  padding: 0.5rem 0.7rem;
  border-radius: 10px;
  border: 3px solid transparent;
  box-shadow: 0 4px 8px rgba(27, 27, 27, 0.3);
}
.project-member {
  border: 3px solid rgba(255, 255, 255, 0.6);
}
.selected-employee {
  border: 3px solid rgba(255, 95, 30, 0.6);
}
.employee-item:last-child {
  margin-bottom: 0;
}
.roles-container {
  display: flex;
  flex-direction: column;
  width: 40%;
  padding: 0.5rem 0 0 1rem;
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
.button {
  margin-top: auto;
}
</style>
