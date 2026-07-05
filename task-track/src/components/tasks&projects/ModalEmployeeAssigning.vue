<template>
  <teleport to="body">
    <div
      class="modal-background"
      @click="$emit('update:modelValue', false)"
    ></div>
    <dialog open>
      <div class="asssigning-container">
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
        <div class="roles-container"></div>
      </div>
    </dialog>
  </teleport>
</template>

<script setup>
import { onMounted, onUnmounted } from "vue";
import { useStoreEmployee } from "@/stores/storeEmployee";
import { useStoreProjects } from "@/stores/storeProjects";

// data
const employeeStore = useStoreEmployee();
const projectsStore = useStoreProjects();

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
    emit("update:modelValue", false);
  }
};

// load when mount
onMounted(async () => {
  document.addEventListener("keyup", handleKeybord);

  if (!employeeStore.employeesLoaded) {
    await employeeStore.getAllEmployees();
  }
  await projectsStore.getAllRoles();
  console.log(employeeStore.otherEmployees);
  console.log(projectsStore.roles);
});

onUnmounted(() => {
  document.removeEventListener("keyup", handleKeybord);
});
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
</style>
