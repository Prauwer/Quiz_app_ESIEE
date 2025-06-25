<template>
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
  <router-link to="/new-quiz">Démarrer le quiz !</router-link>
</template>

<script setup>
import { ref, onMounted } from 'vue';

/////BACK COMMENTÉ/////
// import quizApiService from '@/services/QuizApiService.js';

import scoresData from '@/data/scores.json';

const registeredScores = ref([]);

onMounted(async () => {
  /////BACK COMMENTÉ/////
  // try {
  //   const response = await quizApiService.getScore();
  //   registeredScores.value = response.data;
  //   console.log('Registered scores:', registeredScores.value);
  // } catch (error) {
  //   console.error('Error fetching registered scores:', error);
  // }

  registeredScores.value = scoresData;
  console.log('Registered scores (from JSON):', registeredScores.value);
});
</script>

<style lang="scss" scoped></style>
