<template>
  <div class="question-manager-page bg-light py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow-sm">
            <div class="card-header bg-primary text-white d-flex justify-content-between">
              <h1 class="h4 mb-0">
                Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}
              </h1>
            </div>
            <div class="card-body p-4">
              <div v-if="currentQuestion">
                <QuestionDisplay
                  :currentQuestion="currentQuestion"
                  @answer-clicked="answerClickedHandler"
                />
              </div>
              <div v-else class="text-center text-muted">
                <p>Chargement du quiz...</p>
                <div class="spinner-border" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, onBeforeRouteLeave } from 'vue-router';
import quizApiService from '@/services/QuizApiService.js';
import participationStorageService from '@/services/ParticipationStorageService.js';
import QuestionDisplay from '@/components/QuestionDisplay.vue';

const allQuestions = ref([]);
const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);
const playerAnswers = ref([]);
const isQuizInProgress = ref(false);
const router = useRouter();

onMounted(async () => {
  try {
    const infoResponse = await quizApiService.getQuizInfo();
    const quizSize = infoResponse.data.size;
    totalNumberOfQuestions.value = quizSize;
    if (quizSize === 0) return;
    const fetchPromises = [];
    for (let i = 1; i <= quizSize; i++) {
      fetchPromises.push(quizApiService.getQuestionByPosition(i));
    }
    const questionResponses = await Promise.all(fetchPromises);
    allQuestions.value = questionResponses.map((response) => response.data);
    loadQuestionByPosition(currentQuestionPosition.value);
    isQuizInProgress.value = true;
  } catch (error) {
    console.error("Erreur lors de l'initialisation du quiz:", error);
  }
});

function loadQuestionByPosition(position) {
  currentQuestion.value = allQuestions.value[position - 1];
}

function answerClickedHandler(selectedAnswerId) {
  playerAnswers.value.push(selectedAnswerId);
  if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
    currentQuestionPosition.value++;
    loadQuestionByPosition(currentQuestionPosition.value);
  } else {
    endQuiz();
  }
}

async function endQuiz() {
  isQuizInProgress.value = false;
  try {
    const playerName = participationStorageService.getPlayerName();
    const response = await quizApiService.saveParticipation({
      playerName: playerName,
      answers: playerAnswers.value,
    });
    participationStorageService.saveParticipationScore(response.data.score);
  } catch (error) {
    console.error('Erreur lors de la sauvegarde de la participation:', error);
  }
  router.push('/score');
}

onBeforeRouteLeave((to, from, next) => {
  if (isQuizInProgress.value) {
    if (window.confirm('Voulez-vous vraiment quitter ? Votre progression sera perdue.')) {
      next();
    } else {
      next(false);
    }
  } else {
    next();
  }
});
</script>

<style lang="scss" scoped>
.question-manager-page {
  display: flex;
  align-items: center;
  min-height: 100vh;
}
</style>
