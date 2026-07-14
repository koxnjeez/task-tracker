<template>
  <teleport to="body">
    <div class="modal-background" @click="closeModal"></div>
    <dialog open>
      <div class="adding-container">
        <input
          type="text"
          class="new-status-input"
          :class="{ error: statusValidationError }"
          placeholder="Status name..."
          ref="newStatusInputRef"
          v-model="newStatusInput"
          @click="statusValidationError = false"
        />
        <button class="button button-dark" @click="addNewStatus">Add</button>
      </div>
      <p class="error-message" v-if="statusValidationError">
        Status input can't be empty or oversized! (1-50 symbols)
      </p>
      <div class="statuses-container">
        <ul class="statuses-list">
          <li
            class="status-item"
            v-for="status in statusesStore.statuses"
            :key="status.id"
          >
            <div class="status-title">
              {{ status.title }}
            </div>
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              @click="deleteStatus(status.id)"
            >
              <path
                d="M6 6V17.8C6 18.9201 6 19.4798 6.21799 19.9076C6.40973 20.2839 6.71547 20.5905 7.0918 20.7822C7.5192 21 8.07899 21 9.19691 21H14.8031C15.921 21 16.48 21 16.9074 20.7822C17.2837 20.5905 17.5905 20.2839 17.7822 19.9076C18 19.4802 18 18.921 18 17.8031V6M6 6H8M6 6H4M8 6H16M8 6C8 5.06812 8 4.60241 8.15224 4.23486C8.35523 3.74481 8.74432 3.35523 9.23438 3.15224C9.60192 3 10.0681 3 11 3H13C13.9319 3 14.3978 3 14.7654 3.15224C15.2554 3.35523 15.6447 3.74481 15.8477 4.23486C15.9999 4.6024 16 5.06812 16 6M16 6H18M18 6H20"
                stroke="white"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </li>
        </ul>
      </div>
    </dialog>
  </teleport>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useStoreStatuses } from "@/stores/storeStatuses";
import { useRoute } from "vue-router";

// data
const statusesStore = useStoreStatuses();
const route = useRoute();
const projectId = parseInt(route.params.id);
const newStatusInputRef = ref(null);
const newStatusInput = ref("");
const statusValidationError = ref(false);

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
  // дозаполнить
  emit("update:modelValue", false);
};

// alternative close
const handleKeybord = (e) => {
  if (e.key === "Escape") {
    closeModal();
  }
};

onMounted(async () => {
  document.addEventListener("keyup", handleKeybord);

  if (!statusesStore.statusesLoaded) {
    await statusesStore.fetchStatuses(projectId);
  }

  setTimeout(() => {
    if (newStatusInputRef.value) {
      newStatusInputRef.value.focus();
    }
  }, 50);
});

onUnmounted(() => {
  document.removeEventListener("keyup", handleKeybord);
});

const addNewStatus = async () => {
  newStatusInput.value = newStatusInput.value.trim();

  if (newStatusInput.value.length === 0 || newStatusInput.value.length > 50) {
    statusValidationError.value = true;
    return;
  }

  const statement = {
    title: newStatusInput.value,
  };

  try {
    await statusesStore.createNewStatus(projectId, statement);
    newStatusInput.value = "";
  } catch (error) {
    console.error("Failed new status adding:", error);
    throw error;
  }
};

const deleteStatus = async (status_id) => {
  try {
    await statusesStore.deleteStatus(projectId, status_id);
  } catch (error) {
    console.error("Failed status deleting:", error);
    throw error;
  }
};
</script>

<style scoped>
dialog {
  width: 35%;
}
.adding-container {
  display: flex;
  gap: 1rem;
}
.new-status-input {
  height: 3rem;
  width: 100%;
}
.statuses-container {
  background: rgba(255, 255, 255, 0.3);
  height: 20rem;
  border-radius: 10px;
  margin-top: 0.5rem;
}
.statuses-list {
  margin: 0;
  padding: 0.5rem;
}
.status-item {
  list-style: none;
  background: rgba(0, 0, 0, 0.6);
  margin-bottom: 0.3rem;
  padding: 0.5rem 0.7rem;
  border-radius: 10px;
  border: 3px solid transparent;
  box-shadow: 0 4px 8px rgba(27, 27, 27, 0.3);
  display: flex;
  justify-content: space-between;
}
svg {
  cursor: pointer;
}
</style>
