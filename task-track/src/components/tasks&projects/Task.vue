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
    <button
      class="task-assignees-section"
      @click.stop="$emit('openTaskAssigning')"
    >
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M21 19.9999C21 18.2583 19.3304 16.7767 17 16.2275M15 20C15 17.7909 12.3137 16 9 16C5.68629 16 3 17.7909 3 20M15 13C17.2091 13 19 11.2091 19 9C19 6.79086 17.2091 5 15 5M9 13C6.79086 13 5 11.2091 5 9C5 6.79086 6.79086 5 9 5C11.2091 5 13 6.79086 13 9C13 11.2091 11.2091 13 9 13Z"
          stroke="white"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </button>
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

// emits
const emit = defineEmits(["openTaskAssigning"]);
</script>

<style scoped>
.task-card {
  display: flex;
  gap: 1.5rem;
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
.task-assignees-section {
  background: transparent;
  border: none;
  height: fit-content;
  cursor: pointer;
}
</style>
