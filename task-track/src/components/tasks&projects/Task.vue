<template>
  <div class="task-card">
    <div class="task-id-section">
      {{ task.id }}
    </div>
    <div class="task-title-section">
      {{ task.title }}
    </div>
    <div class="task-description-section">
      {{ task.description }}
    </div>
    <div class="task-status-section">
      {{ task.status }}
    </div>
    <div class="task-date-section">
      {{ task.start_date }}
    </div>
    <div class="task-date-section">
      {{ task.end_date }}
    </div>
    <div class="task-pull-request-section">
      {{ task.pull_request }}
    </div>
  </div>
</template>

<script setup>
// props
const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.task-card {
  display: flex;
  gap: 0.5rem;
  padding: 0 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.7);
  cursor: pointer;
}
.task-card:last-child {
  border-bottom: none;
}
.task-card [class^="task"] {
  padding: 1rem 0;
}
.task-id-section {
  width: 3%;
}
.task-title-section {
  width: 20%;
}
.task-description-section {
  width: 30%;
}
.task-status-section {
  width: 12%;
  text-transform: uppercase;
}
.task-date-section {
  width: 10%;
}
.task-pull-request-section {
  width: 15%;
}
</style>
