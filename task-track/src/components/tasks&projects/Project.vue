<template>
  <div class="project-card">
    <div class="project-id-section">
      {{ project.id }}
    </div>
    <div class="project-title-section">
      {{ project.title }}
    </div>
    <div class="project-privacy-section">
      {{ project.is_private ? "Private" : "Public" }}
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  project: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.project-card {
  display: flex;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.7);
}
.project-id-section {
  width: 10%;
}
.project-title-section {
  width: 80%;
}
.project-privacy-section {
  width: 10%;
}
</style>
