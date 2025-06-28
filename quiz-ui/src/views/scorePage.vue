<template>
  <div class="score-page py-5 bg-light">
    <div class="container">
      <div class="row">
        <div class="col-md-8 offset-md-2">
          <div class="card text-center shadow-sm">
            <div class="card-body p-5">
              <div v-if="playerName">
                <h1 class="card-title">🏆 Bravo, {{ playerName }} ! 🏆</h1>
                <p class="lead text-muted">Vous avez terminé le quiz avec brio.</p>

                <div class="my-4">
                  <p class="mb-2">Votre score final est de :</p>
                  <h2 class="display-3 fw-bold text-primary">{{ score }} / {{ totalQuestions }}</h2>
                </div>

                <div class="alert alert-info" role="alert">
                  <h4 class="alert-heading">Votre classement</h4>
                  <p>
                    Vous êtes classé(e) <strong>#{{ playerRank }}</strong> parmi tous les
                    participants.
                  </p>
                  <hr />
                  <p class="mb-0">{{ feedbackMessage }}</p>
                </div>

                <hr class="my-4" />

                <h3 class="mb-3">Leaderboard - Top 3</h3>
                <div v-if="topThreeScores.length > 0">
                  <ul class="list-group list-group-flush">
                    <li
                      v-for="(scoreEntry, index) in topThreeScores"
                      :key="scoreEntry.date"
                      class="list-group-item d-flex justify-content-between align-items-center"
                      :class="{ 'list-group-item-success': scoreEntry.playerName === playerName }"
                    >
                      <span class="fw-bold">
                        <span v-if="index === 0">🥇</span>
                        <span v-else-if="index === 1">🥈</span>
                        <span v-else-if="index === 2">🥉</span>
                        {{ scoreEntry.playerName }}
                      </span>
                      <span class="badge bg-primary rounded-pill fs-6"
                        >{{ scoreEntry.score }} pts</span
                      >
                    </li>
                  </ul>
                </div>
                <p v-else>Le classement est en cours de chargement...</p>

                <div class="d-grid gap-2 d-sm-flex justify-content-sm-center mt-4">
                  <button @click="playAgain" class="btn btn-primary btn-lg px-4 gap-3">
                    Rejouer
                  </button>
                  <router-link to="/" class="btn btn-secondary btn-lg px-4"
                    >Retour à l'accueil</router-link
                  >
                </div>
              </div>

              <div v-else>
                <h1 class="card-title">Quiz terminé</h1>
                <p class="lead">Aucune donnée de participation n'a été trouvée.</p>
                <router-link to="/" class="btn btn-secondary mt-3">Retour à l'accueil</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService.js';
import quizApiService from '@/services/QuizApiService.js';

const router = useRouter();
const playerName = ref('');
const score = ref(0);
const totalQuestions = ref(0);
const allScores = ref([]);

onMounted(async () => {
  // Récupérer les informations du joueur depuis le stockage local
  playerName.value = participationStorageService.getPlayerName();
  score.value = participationStorageService.getParticipationScore();

  // Récupérer les informations générales du quiz (y compris les scores)
  try {
    const response = await quizApiService.getQuizInfo();
    allScores.value = response.data.scores;
    totalQuestions.value = response.data.size;
  } catch (error) {
    console.error('Erreur lors de la récupération des informations du quiz:', error);
    // Optionnel : afficher un message d'erreur à l'utilisateur
  }
});

// Calcule le classement du joueur
const playerRank = computed(() => {
  const sortedScores = [...allScores.value].sort((a, b) => b.score - a.score);
  const playerIndex = sortedScores.findIndex(
    (s) => s.playerName === playerName.value && s.score === score.value
  );
  return playerIndex !== -1 ? playerIndex + 1 : 'N/A';
});

// Calcule les 3 meilleurs scores
const topThreeScores = computed(() => {
  return [...allScores.value].sort((a, b) => b.score - a.score).slice(0, 3);
});

// Calcule un message de feedback en fonction du score
const feedbackMessage = computed(() => {
  if (totalQuestions.value === 0) return 'Le quiz ne semble pas contenir de questions.';
  const percentage = (score.value / totalQuestions.value) * 100;
  if (percentage === 100) return 'Parfait ! Vous êtes un véritable maître du quiz !';
  if (percentage >= 75) return 'Excellent score ! Vous avez de solides connaissances.';
  if (percentage >= 50) return 'Pas mal du tout ! Continuez comme ça.';
  return "Vous pouvez faire mieux. N'hésitez pas à retenter votre chance !";
});

// Fonction pour rejouer
function playAgain() {
  // On ne nettoie que le score, le nom peut être conservé pour la prochaine partie
  participationStorageService.clear();
  router.push('/new-quiz');
}
</script>

<style scoped>
/* Scoped styles pour des ajustements fins si nécessaire */
.score-page {
  min-height: 100vh;
  width: 100% !important;
}
.display-3 {
  font-weight: 700;
}
.list-group-item-success {
  background-color: #e9f7ef; /* Un vert léger pour mettre en évidence le joueur actuel */
}
</style>
