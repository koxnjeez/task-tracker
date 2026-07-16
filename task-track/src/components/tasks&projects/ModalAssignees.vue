<template>
  <teleport to="body">
    <div class="modal-background" @click="closeModal"></div>
    <dialog open>
      <div class="assignees-section">
        <div class="available-assignees">
          <h4>Available assignees</h4>
          <div class="employees-section">
            <ul class="assignee-list">
              <li
                class="assignee-item list-item"
                v-for="assignee in employeeStore.unassigned"
                :key="assignee.id"
                @click="
                  employeeStore.assignEmployee(
                    assignee,
                    props.taskId,
                    projectId,
                  )
                "
              >
                {{ assignee.first_name }} {{ assignee.last_name }}
                {{ assignee.middle_name }}
              </li>
            </ul>
          </div>
        </div>
        <div class="busy-assignees">
          <h4>Assignees on the task</h4>
          <div class="employees-section">
            <ul class="assignee-list">
              <li
                class="assignee-item list-item"
                v-for="assignee in employeeStore.assigned"
                :key="assignee.id"
                @click="
                  employeeStore.unassignEmployee(
                    assignee,
                    props.taskId,
                    projectId,
                  )
                "
              >
                {{ assignee.first_name }} {{ assignee.last_name }}
                {{ assignee.middle_name }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </dialog>
  </teleport>
</template>

<script setup>
import { onMounted, onUnmounted } from "vue";
import { useStoreEmployee } from "@/stores/storeEmployee";
import { useRoute } from "vue-router";

// data
const employeeStore = useStoreEmployee();
const route = useRoute();
const projectId = parseInt(route.params.id);

// props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  taskId: {
    type: Number,
    required: true,
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
  // дозаполнить
  emit("update:modelValue", false);
};

// load when mount
onMounted(async () => {
  document.addEventListener("keyup", handleKeybord);

  await employeeStore.fetchAssigneesData(props.taskId, projectId);
});

onUnmounted(() => {
  document.removeEventListener("keyup", handleKeybord);
});
</script>

<style scoped>
dialog {
  width: 45%;
}
.assignees-section {
  display: flex;
  gap: 1.5rem;
}
.available-assignees {
  width: 50%;
}
.busy-assignees {
  width: 50%;
}
.employees-section {
  background: rgba(255, 255, 255, 0.3);
  height: 15rem;
  border-radius: 10px;
}
h4 {
  margin: 0 0 1rem 0;
}
.assignee-list {
  padding: 0.5rem;
  margin: 0;
}
</style>
