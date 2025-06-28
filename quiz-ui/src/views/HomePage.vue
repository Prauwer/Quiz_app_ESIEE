<template>
  <div>
    <h1>Tableau des Scores</h1>
    <div v-if="registeredScores.length > 0">
      <ul>
        <li v-for="scoreEntry in registeredScores" :key="scoreEntry.date">
          {{ scoreEntry.playerName }} - {{ scoreEntry.score }} ({{ scoreEntry.date }})
        </li>
      </ul>
    </div>
    <p v-else>Aucun score enregistré pour le moment.</p>
    <router-link to="/new-quiz">Démarrer le quiz !</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService.js';

const registeredScores = ref([]);

onMounted(async () => {
  try {
    const response = await quizApiService.getQuizInfo();
    registeredScores.value = response.data.scores;
  } catch (error) {
    console.error('Erreur lors de la récupération des scores:', error);
  }
});
</script>

<style lang="scss" scoped></style>
