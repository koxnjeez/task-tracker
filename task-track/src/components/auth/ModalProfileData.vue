<template>
  <teleport to="body">
    <div
      class="modal-background"
      v-if="modelValue"
      @click="$emit('update:modelValue', false)"
    ></div>
    <dialog open v-if="modelValue">
      <section class="edit-data-title">Edit your personal data:</section>
      <form @submit.prevent="savePersonalDataForm" class="personal-data-form">
        <label for="first-name">First name</label>
        <input type="text" id="first-name" v-model="firstName" />
        <label for="last-name">Last name</label>
        <input type="text" id="last-name" v-model="lastName" />
        <label for="middle-name">Middle name</label>
        <input type="text" id="middle-name" v-model="middleName" />
        <label for="phone-number">Phone number</label>
        <input type="text" id="phone-number" v-model="phoneNumber" />
        <button class="button button-dark">Save data</button>
      </form>
    </dialog>
  </teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useStoreEmployee } from "@/stores/storeEmployee";

// props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
});

// emits
const emit = defineEmits(["update:modelValue"]);

// data
const employeeStore = useStoreEmployee();
const firstName = ref("");
const lastName = ref("");
const middleName = ref("");
const phoneNumber = ref("");

// alternative close
const handleKeybord = (e) => {
  if (e.key === "Escape") {
    emit("update:modelValue", false);
  }
};

// load when mount
onMounted(() => {
  firstName.value = employeeStore.user.first_name;
  lastName.value = employeeStore.user.last_name;
  middleName.value = employeeStore.user.middle_name;
  phoneNumber.value = employeeStore.user.phone_number;

  document.addEventListener("keyup", handleKeybord);
});

onUnmounted(() => {
  document.removeEventListener("keyup", handleKeybord);
});

// edited form saving
const savePersonalDataForm = () => {};
</script>

<style scoped>
.modal-background {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100vh;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(2px);
}
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
  width: 20%;
  max-width: 20rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(27, 27, 27, 0.3);
}
.edit-data-title {
  font-weight: 700;
  font-size: 20px;
  margin-bottom: 1.5rem;
}
.personal-data-form {
  display: flex;
  flex-direction: column;
}
.personal-data-form input {
  margin-bottom: 0.75rem;
  height: 1.8rem;
  padding-left: 0.5rem;
  background: rgba(255, 255, 255, 0.4);
  color: black;
  box-shadow: 0 4px 8px rgba(27, 27, 27, 0.3);
  backdrop-filter: blur(16px);
  outline: none;
  font-family: inherit;
  font-size: 16px;
  font-weight: 500;
  border: none;
  border-radius: 5px;
}
.button {
  margin-top: 1rem;
}
</style>
