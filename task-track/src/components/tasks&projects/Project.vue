<template>
  <div class="project-card">
    <div class="project-id-section">
      {{ project.id }}
    </div>
    <div
      class="project-title-section"
      @click="router.push(`/projects/${project.id}`)"
    >
      {{ project.title }}
    </div>
    <div class="project-privacy-section">
      {{ project.is_private ? "Private" : "Public" }}
    </div>
    <div class="icons-section">
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        @click="$emit('updateProject')"
      >
        <path
          d="M12 8.00012L4 16.0001V20.0001L8 20.0001L16 12.0001M12 8.00012L14.8686 5.13146L14.8704 5.12976C15.2652 4.73488 15.463 4.53709 15.691 4.46301C15.8919 4.39775 16.1082 4.39775 16.3091 4.46301C16.5369 4.53704 16.7345 4.7346 17.1288 5.12892L18.8686 6.86872C19.2646 7.26474 19.4627 7.46284 19.5369 7.69117C19.6022 7.89201 19.6021 8.10835 19.5369 8.3092C19.4628 8.53736 19.265 8.73516 18.8695 9.13061L18.8686 9.13146L16 12.0001M12 8.00012L16 12.0001"
          stroke="white"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </div>
  </div>
</template>

<script setup>
import router from "@/router";

// props
const props = defineProps({
  project: {
    type: Object,
    required: true,
  },
});

// emits
const emit = defineEmits("updateProject");
</script>

<style scoped>
.project-card {
  display: flex;
  gap: 0.5rem;
  padding: 0 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.7);
}
.project-card:last-child {
  border-bottom: none;
}
.project-card [class^="project"] {
  padding: 1rem 0;
}
.project-id-section {
  width: 10%;
}
.project-title-section {
  width: 75%;
  cursor: pointer;
}
.project-privacy-section {
  width: 15%;
}
.icons-section {
  height: 1.5rem;
  position: absolute;
  right: 3.5rem;
  transform: translateY(1rem);
}
.icons-section svg {
  cursor: pointer;
}
</style>
