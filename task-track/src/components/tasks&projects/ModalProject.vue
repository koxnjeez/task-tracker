<template>
  <teleport to="body">
    <div class="modal-background" @click="closeModal"></div>
    <dialog open>
      <section class="add_project_title">Add new project</section>
      <form @submit.prevent="createNewProject" class="add_project_form">
        <label for="project_title">Project title</label>
        <input
          type="text"
          id="project_title"
          v-model="projectTitle"
          ref="titleInputFieldRef"
        />
        <label>Project privacy</label>
        <label class="switch">
          <input type="checkbox" v-model="projectPrivacy" />
          <span class="slider"></span>
        </label>
        <button class="button button-dark">Save</button>
      </form>
    </dialog>
  </teleport>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useStoreProjects } from "@/stores/storeProjects";

// data
const projectTitle = ref("");
const projectPrivacy = ref(false);
const titleInputFieldRef = ref(null);
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

// modal close
const closeModal = () => {
  projectTitle.value = "";
  projectPrivacy.value = false;
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
const createNewProject = async () => {
  projectTitle.value = projectTitle.value.trim();

  if (projectTitle.value.length === 0) {
    alert("You can't create a project without the name!");
    return;
  } else if (projectTitle.value.length > 255) {
    alert("The maximum length of a project title is 255 symbols.");
    return;
  }

  const statement = {
    title: projectTitle.value,
    is_private: projectPrivacy.value,
  };

  try {
    await projectsStore.createNewProject(statement);
    closeModal();
  } catch (error) {
    console.error("Project creating error:", error);
    alert("Something goes wrong while creating the project!");
  }
};
</script>

<style scoped>
dialog {
  position: fixed;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  border: none;
  width: 70%;
  /* max-width: 20rem; */
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(27, 27, 27, 0.3);
}
.add_project_title {
  justify-self: center;
  font-weight: 700;
  margin-bottom: 1.5rem;
}
.add_project_form {
  display: flex;
  flex-direction: column;
}
[type="text"],
.switch {
  margin: 0.25rem 0 1rem 0;
  height: 1.8rem;
  outline: none;
  border: none;
}
[type="text"] {
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
.switch {
  position: relative;
  display: inline-block;
  width: 3.6rem;
}
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 34px;
  transition: 0.3s;
}
.slider:before {
  position: absolute;
  content: "";
  height: 1.3rem;
  width: 1.3rem;
  left: 0.25rem;
  bottom: 0.25rem;
  background: rgba(255, 255, 255, 0.6);
  transition: 0.3s;
  border-radius: 50%;
}
input:checked + .slider {
  background: rgba(255, 95, 30, 0.6);
}
input:checked + .slider:before {
  transform: translateX(1.8rem);
}
</style>
