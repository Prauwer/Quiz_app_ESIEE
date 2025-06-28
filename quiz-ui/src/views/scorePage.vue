<template>
  <div class="score-container" v-if="playerName">
    <h1>🏆 Bravo, {{ playerName }} ! 🏆</h1>
    <p style="color: #205b40">Vous avez terminé le quiz.</p>
    <div class="score-display">
      <p>Votre score final est de :</p>
      <span class="score">{{ score }} / {{ totalQuestions }}</span>
    </div>

    <div class="feedback">
      <p>{{ feedbackMessage }}</p>
    </div>
    <div class="registered-scores">
      <h2>tableaux des scores</h2>
      <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </div>
    </div>

    <div class="actions">
      <button @click="playAgain">Rejouer</button>
      <router-link to="/" class="button-secondary">Retour à l'accueil</router-link>
    </div>
  </div>
  <div v-else class="score-container">
    <h1>Quiz terminé</h1>
    <p>Aucune donnée de participation trouvée.</p>
    <router-link to="/" class="button-secondary">Retour à l'accueil</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService.js';
import quizData from '@/data/questions.json'; // Pour obtenir le nombre total de questions
import quizApiService from '@/services/QuizApiService.js';

const router = useRouter();
const playerName = ref('');
const score = ref(0);
const totalQuestions = ref(0);
const registeredScores = ref([]);

onMounted(async () => {
  try {
    const response = await quizApiService.getQuizInfo();
    registeredScores.value = response.data.scores;
  } catch (error) {
    console.error('Erreur:', error);
  }
});

// onMounted est appelé lorsque le composant est prêt
onMounted(() => {
  playerName.value = participationStorageService.getPlayerName();
  score.value = participationStorageService.getParticipationScore(); // Assure que le score est un nombre
  totalQuestions.value = quizData.questions.length;
});

// Calcule un message de feedback en fonction du score
const feedbackMessage = computed(() => {
  if (totalQuestions.value === 0) return '';
  const percentage = (score.value / totalQuestions.value) * 100;
  if (percentage === 100) {
    return 'Parfait ! Vous êtes un véritable maître du quiz !';
  } else if (percentage >= 75) {
    return 'Excellent score ! Vous avez de solides connaissances.';
  } else if (percentage >= 50) {
    return 'Pas mal du tout ! Continuez comme ça.';
  } else {
    return "Vous pouvez faire mieux. N'hésitez pas à retenter votre chance !";
  }
});

// Fonction pour rejouer
function playAgain() {
  // On nettoie les données de la partie précédente
  participationStorageService.clear();
  // On redirige vers la page pour démarrer un nouveau quiz
  router.push('/new-quiz');
}
</script>

<style lang="scss" scoped>
.score-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  color: #333;
}

.score-display {
  margin: 20px 0;
  p {
    margin: 0;
    font-size: 1.2em;
    color: #205b40;
  }
  .score {
    font-size: 3em;
    font-weight: bold;
    color: #42b983;
  }
}

.feedback {
  font-style: italic;
  color: #555;
  margin-bottom: 30px;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 20px;

  button,
  .button-secondary {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-size: 1em;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
  }

  button {
    background-color: #42b983;
    color: white;
    transition: background-color 0.3s;

    &:hover {
      background-color: #369b70;
    }
  }

  .button-secondary {
    background-color: #ccc;
    color: #333;
    transition: background-color 0.3s;

    &:hover {
      background-color: #bbb;
    }
  }
}
</style>
