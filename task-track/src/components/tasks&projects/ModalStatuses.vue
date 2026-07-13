<template>
  <teleport to="body">
    <div class="modal-background" @click="closeModal"></div>
    <dialog open></dialog>
  </teleport>
</template>

<script setup>
import { onMounted, onUnmounted } from "vue";

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
});

onUnmounted(() => {
  document.removeEventListener("keyup", handleKeybord);
});
</script>

<style scoped>
dialog {
  width: 50%;
}
</style>
