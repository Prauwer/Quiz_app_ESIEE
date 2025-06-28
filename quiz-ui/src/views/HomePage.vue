<template>
  <div class="home-page bg-light">
    <div class="container py-5">
      <div class="row">
        <div class="col-md-8 offset-md-2 text-center">
          <h1 class="display-4 fw-bold">Bienvenue au Super Quiz !</h1>
          <p class="lead text-muted">
            Testez vos connaissances et tentez d'atteindre le sommet du classement.
          </p>

          <div class="my-4">
            <router-link to="/new-quiz" class="btn btn-primary btn-lg px-5 py-3 shadow-sm">
              Démarrer le quiz !
            </router-link>
          </div>

          <div class="card shadow-sm">
            <div class="card-header">
              <h2 class="h4 mb-0">Tableau des Scores</h2>
            </div>
            <div v-if="registeredScores.length > 0" class="card-body p-0">
              <ul class="list-group list-group-flush">
                <li
                  v-for="scoreEntry in sortedScores"
                  :key="scoreEntry.date"
                  class="list-group-item d-flex justify-content-between align-items-center"
                >
                  <div>
                    <span class="fw-bold">{{ scoreEntry.playerName }}</span>
                    <br />
                  </div>
                  <span class="badge bg-secondary rounded-pill fs-6"
                    >{{ scoreEntry.score }} pts</span
                  >
                </li>
              </ul>
            </div>
            <div v-else class="card-body">
              <p class="mb-0">Aucun score n'est enregistré pour le moment. Soyez le premier !</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import quizApiService from '@/services/QuizApiService.js';

const registeredScores = ref([]);

onMounted(async () => {
  try {
    const response = await quizApiService.getQuizInfo();
    // La réponse de l'API donne les scores, on les stocke
    registeredScores.value = response.data.scores;
  } catch (error) {
    console.error('Erreur lors de la récupération des scores:', error);
  }
});

// Trie les scores du plus haut au plus bas
const sortedScores = computed(() => {
  return [...registeredScores.value].sort((a, b) => b.score - a.score);
});

// Formate la date pour une meilleure lisibilité
function formatDate(dateString) {
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  };
  return new Date(dateString).toLocaleDateString('fr-FR', options);
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}
.btn-primary {
  font-weight: bold;
  letter-spacing: 0.5px;
}
.list-group-item div {
  text-align: left;
}
</style>
