<template>
  <teleport to="body">
    <div class="modal-background" @click="closeModal"></div>
    <dialog open>
      <section class="project_title">Customize your project</section>
      <form @submit.prevent="saveProject" class="project_form">
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
  editingProject: {
    type: Object,
    default: null,
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
  if (props.editingProject) {
    projectTitle.value = props.editingProject.title || "";
    projectPrivacy.value = props.editingProject.is_private || false;
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
const saveProject = async () => {
  projectTitle.value = projectTitle.value.trim();

  if (projectTitle.value.length === 0) {
    alert("You can't create a project without the name!");
    return;
  } else if (projectTitle.value.length > 255) {
    alert("The maximum length of a project title is 255 symbols.");
    return;
  }

  if (props.editingProject) {
    const statement = {
      id: props.editingProject.id,
    };
    if (projectTitle.value !== props.editingProject.title) {
      statement.title = projectTitle.value;
    }
    if (projectPrivacy.value !== props.editingProject.is_private) {
      statement.is_private = projectPrivacy.value;
    }

    try {
      await projectsStore.updateProjectInfo(statement);
      closeModal();
    } catch (error) {
      console.error("Project updating error:", error);
      alert("Something goes wrong while updating the project!");
    }
  } else {
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
  }
};
</script>

<style scoped>
dialog {
  width: 70%;
  /* max-width: 20rem; */
}
.project_title {
  justify-self: center;
  font-weight: 700;
  margin-bottom: 1.5rem;
}
.project_form {
  display: flex;
  flex-direction: column;
}
[type="text"] {
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
  margin: 0.25rem 0 1rem 0;
}
</style>
