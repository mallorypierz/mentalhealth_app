<script setup>
const emit = defineEmits(['practice']);
const futureExercises = ['5-4-3-2-1 sensory grounding', 'STOP', 'One-minute cognitive reframe'];
</script>

<template>
  <section class="history-card" aria-labelledby="library-heading">
    <h1 id="library-heading">Exercise library</h1>
    <ul class="exercise-library">
      <li>
        <h2>Paced breathing (4–6)</h2>
        <p>Available · 60 seconds · 6 cycles</p>
        <button class="primary" @click="emit('practice')">Open breathing practice</button>
      </li>
      <li v-for="name in futureExercises" :key="name">
        <h2>{{ name }}</h2>
        <p class="status-chip">Coming later · Unavailable</p>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.exercise-library { list-style: none; padding: 0; margin: 0; }
.exercise-library > li { padding: 1.25rem 0; border-top: 1px solid #dce3d6; }
.exercise-library h2 { font-size: 1.3rem; overflow-wrap: anywhere; }
.exercise-library button { max-width: 100%; white-space: normal; }
</style>
