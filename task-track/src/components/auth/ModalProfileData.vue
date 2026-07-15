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
const savePersonalDataForm = async () => {
  const changedFields = {};

  if (firstName.value !== employeeStore.user.first_name) {
    changedFields.first_name = firstName.value;
  }
  if (lastName.value !== employeeStore.user.last_name) {
    changedFields.last_name = lastName.value;
  }
  if (middleName.value !== employeeStore.user.middle_name) {
    changedFields.middle_name = middleName.value;
  }
  if (phoneNumber.value !== employeeStore.user.phone_number) {
    changedFields.phone_number = phoneNumber.value;
  }

  if (Object.keys(changedFields).length === 0) {
    emit("update:modelValue", false);
    return;
  }

  try {
    await employeeStore.updatePersonalInfo(changedFields);
    emit("update:modelValue", false);
  } catch (error) {
    console.error("Update personal info error:", error);
    alert("Something goes wrong while saving the data!");
  }
};
</script>

<style scoped>
dialog {
  width: 20%;
  max-width: 20rem;
  min-width: 16.5rem;
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
[type="text"] {
  margin-bottom: 0.75rem;
}
.button {
  margin-top: 1rem;
}
</style>
