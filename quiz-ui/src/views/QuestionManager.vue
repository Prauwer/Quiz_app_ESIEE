<template>
  <div v-if="currentQuestion">
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
    <QuestionDisplay :currentQuestion="currentQuestion" @answer-clicked="answerClickedHandler" />
  </div>
  <div v-else>
    <p>Chargement du quiz...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, onBeforeRouteLeave } from 'vue-router';
import quizApiService from '@/services/QuizApiService.js';
import participationStorageService from '@/services/ParticipationStorageService.js';
import QuestionDisplay from '@/components/QuestionDisplay.vue';

// Propriétés réactives
const allQuestions = ref([]);
const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);
const playerAnswers = ref([]);
const isQuizInProgress = ref(false);
const router = useRouter();

// [TO DO] Méthode appelée au montage du composant
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

function answerClickedHandler(selectedAnswerIndex) {
  playerAnswers.value.push(selectedAnswerIndex);

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
    await quizApiService.saveParticipation({
      playerName: playerName,
      answers: playerAnswers.value,
    });
  } catch (error) {
    console.error('Erreur lors de la sauvegarde de la participation:', error);
  }
  router.push('/score');
}

// Hook de navigation : demander confirmation avant de quitter la page
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

<style lang="scss" scoped></style>
