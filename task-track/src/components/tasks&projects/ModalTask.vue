<template>
  <teleport to="body">
    <div class="modal-background" @click="closeModal"></div>
    <dialog open>
      <section class="task_title">Customize the task</section>
      <form @submit.prevent="saveProject" class="task_form">
        <label for="task-title">Title</label>
        <input type="text" id="task-title" ref="titleInputFieldRef" />
        <label for="task-description">Description</label>
        <input type="text" id="task-description" />
        <label for="task-status">Status</label>
        <select name="status" id="task-status">
          <option value="todo">TO DO</option>
          <option value="inprogress">IN PROGRESS</option>
          <option value="done">DONE</option>
        </select>
        <label for="task-pull-request">Pull request</label>
        <input type="text" id="task-pull-request" />
      </form>
    </dialog>
  </teleport>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";

// data
const titleInputFieldRef = ref(null);

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
  emit("update:modelValue", false);
};

// alternative close
const handleKeybord = (e) => {
  if (e.key === "Escape") {
    closeModal();
  }
};

onMounted(() => {
  if (props.editingTask) {
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
[type="text"] {
  margin: 0.25rem 0 1rem 0;
}
select {
  margin: 0.25rem 0 1rem 0;
  height: 1.8rem;
  outline: none;
  border: none;
  padding-left: 0.5rem;
  background: rgba(255, 255, 255, 0.4);
  box-shadow: 0 4px 8px rgba(27, 27, 27, 0.3);
  color: black;
  backdrop-filter: blur(16px);
  font-family: inherit;
  font-size: 16px;
  font-weight: 500;
  border-radius: 5px;
}
</style>
