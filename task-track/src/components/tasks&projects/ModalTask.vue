<template>
  <teleport to="body">
    <div class="modal-background" @click="closeModal"></div>
    <dialog open>
      <section class="task_title">Customize the task</section>
      <form @submit.prevent="saveTask" class="task_form">
        <label for="task-title">Title</label>
        <input
          type="text"
          id="task-title"
          v-model="form.title"
          ref="titleInputFieldRef"
          :class="{ error: titleValidationError }"
          @click="titleValidationError = false"
        />
        <p class="error-message" v-if="titleValidationError">
          Title can't be empty or oversized! (1-255 symbols)
        </p>
        <label for="task-description">Description</label>
        <textarea id="task-description" v-model="form.description"></textarea>
        <label for="task-status">Status</label>
        <select name="status" id="task-status" v-model="form.status">
          <option value="todo">TO DO</option>
          <option value="inprogress">IN PROGRESS</option>
          <option value="done">DONE</option>
        </select>
        <label for="task-start-date">Start date</label>
        <input
          type="date"
          id="task-start-date"
          :value="form.startDate"
          readonly
        />
        <label for="task-end-date">End date</label>
        <input
          type="date"
          id="task-end-date"
          v-model="form.endDate"
          :class="{ error: endDateValidationError }"
          @click="endDateValidationError = false"
        />
        <p class="error-message" v-if="endDateValidationError">
          End date can't be in the past! (only on or after {{ today }})
        </p>
        <label for="task-pull-request">Pull request</label>
        <input type="text" id="task-pull-request" v-model="form.pullRequest" />
        <button class="button button-dark">Save</button>
      </form>
    </dialog>
  </teleport>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useStoreTasks } from "@/stores/storeTasks";

// data
const tasksStore = useStoreTasks();
const titleInputFieldRef = ref(null);
const today = new Date().toISOString().split("T")[0];
const form = ref({
  title: "",
  description: "",
  status: "",
  startDate: "",
  endDate: "",
  pullRequest: "",
});
const titleValidationError = ref(false);
const endDateValidationError = ref(false);

// props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  editingTask: {
    type: Object,
    default: null,
  },
});

// emits
const emit = defineEmits(["update:modelValue"]);

// modal close
const closeModal = () => {
  // дозаполнить
  emit("update:modelValue", false);
};

// alternative close
const handleKeybord = (e) => {
  if (e.key === "Escape") {
    closeModal();
  }
};

// load when mount
onMounted(() => {
  if (props.editingTask) {
    form.value.title = props.editingTask.title;
    form.value.description = props.editingTask.description || "";
    form.value.status = props.editingTask.status;
    form.value.startDate = props.editingTask.start_date || "";
    form.value.endDate = props.editingTask.end_date || "";
    form.value.pullRequest = props.editingTask.pull_request || "";
  }

  document.addEventListener("keyup", handleKeybord);

  setTimeout(() => {
    if (titleInputFieldRef.value) {
      titleInputFieldRef.value.focus();
    }
  }, 50);
});

onUnmounted(() => {
  document.removeEventListener("keyup", handleKeybord);
});

// creating with entered data
const saveTask = async () => {
  form.value.title = form.value.title.trim();
  form.value.description = form.value.description.trim();
  form.value.pullRequest = form.value.pullRequest.trim();

  if (form.value.title.length === 0 || form.value.title.length > 255) {
    titleValidationError.value = true;
    return;
  }
  if (form.value.endDate && form.value.endDate < today) {
    endDateValidationError.value = true;
    return;
  }

  const statement = {
    title: form.value.title,
    description: form.value.description || null,
    status: form.value.status,
    start_date: null,
    end_date: form.value.endDate || null,
    pull_request: form.value.pullRequest || null,
  };

  try {
    // await ;
    closeModal();
  } catch (error) {
    console.error("Task creating error:", error);
    alert("Something goes wrong while creating the task!");
  }
};
</script>

<style scoped>
dialog {
  width: 70%;
  /* max-width: 20rem; */
}
.task_title {
  justify-self: center;
  font-weight: 700;
  margin-bottom: 1.5rem;
}
.task_form {
  display: flex;
  flex-direction: column;
}
input,
select,
textarea {
  margin: 0.25rem 0 0 0;
  height: 1.8rem;
  outline: none;
  border: none;
  padding: 0 0.5rem;
  background: rgba(255, 255, 255, 0.4);
  box-shadow: 0 4px 8px rgba(27, 27, 27, 0.3);
  color: black;
  backdrop-filter: blur(16px);
  font-family: inherit;
  font-size: 16px;
  font-weight: 500;
  border-radius: 5px;
}
textarea {
  height: 3.6rem;
  padding-top: 0.5rem;
}
label {
  margin-top: 1rem;
}
label:first-child {
  margin: 0;
}
.error-message {
  margin: 0.2rem 0 0 0;
  font-size: small;
  color: rgb(255, 90, 90);
}
.error {
  border: 3px solid rgb(255, 90, 90);
}
.button {
  margin-top: 3rem;
}
</style>
