<template>
  <div v-if="currentQuestion">
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
    <QuestionDisplay :currentQuestion="currentQuestion" @answer-clicked="answerClickedHandler" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
// import quizApiService from '@/services/QuizApiService.js';
import QuestionDisplay from '@/components/QuestionDisplay.vue';
import participationStorageService from '@/services/ParticipationStorageService.js';
import { useRouter, onBeforeRouteLeave } from 'vue-router';

import quizData from '@/data/questions.json';

// Propriétés réactives
const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);
const score = ref(0); // Pour suivre le score
const router = useRouter();

//ajout temporaire pour simuler la récupération des questions
const allQuestions = ref([]);

// Variable pour suivre si un quiz est en cours
const isQuizInProgress = ref(false);

// [TO DO] Méthode appelée au montage du composant
onMounted(async () => {
  // VERSION TEMPORAIRE
  allQuestions.value = quizData.questions; // Simuler la récupération des questions depuis un fichier
  totalNumberOfQuestions.value = allQuestions.value.length;

  if (totalNumberOfQuestions.value > 0) {
    loadQuestionByPosition(currentQuestionPosition.value);
    isQuizInProgress.value = true; // Le quiz commence
  } else {
    console.error('Aucune question disponible.');
  }
});

// Hook de navigation : demander confirmation avant de quitter la page
onBeforeRouteLeave((to, from, next) => {
  if (isQuizInProgress.value) {
    const confirmation = window.confirm(
      'Vous êtes sur le point de quitter le quiz. Votre progression sera perdue. Voulez-vous vraiment continuer ?'
    );
    if (confirmation) {
      isQuizInProgress.value = false; // Réinitialise l'état du quiz
      next(); // Continue la navigation
    } else {
      next(false); // Annule la navigation
    }
  } else {
    next(); // Permet la navigation si le quiz n'est pas en cours
  }
});

// [TO DO] Méthode pour charger une question par sa position (1-based index)
async function loadQuestionByPosition(position) {
  // Ex : récupérer la question depuis une liste locale ou API
  //   const response = await fetch(`/api/questions/${position}`);
  //   currentQuestion.value = await response.json();

  // VERSION TEMPORAIRE
  currentQuestion.value = allQuestions.value[position - 1];
}

// [TO DO] Méthode appelée lorsque l'utilisateur clique sur une réponse
async function answerClickedHandler(selectedAnswerIndex) {
  console.log('Réponse choisie :', selectedAnswerIndex);

  // On vérifie si la réponse est correcte
  if (selectedAnswerIndex === currentQuestion.value.réponse) {
    score.value++;
    console.log('Bonne réponse ! Score actuel :', score.value);
  } else {
    console.log('Mauvaise réponse.');
  }

  // Logique de vérification / passage à la suite
  if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
    currentQuestionPosition.value++;
    loadQuestionByPosition(currentQuestionPosition.value);
  } else {
    endQuiz();
  }
}

// [TO DO]
function endQuiz() {
  console.log('Le quiz est terminé !');
  console.log('Score final :', score.value, '/', totalNumberOfQuestions.value);

  // [AJOUT] On sauvegarde le score et on redirige
  // Note : `participationStorageService` doit avoir une méthode pour sauvegarder le score.
  // Si elle n'existe pas, vous pouvez l'ajouter.
  participationStorageService.saveParticipationScore(score.value);
  isQuizInProgress.value = false; // Le quiz est terminé
  // Redirection vers la page d'accueil (ou une page de résultats)
  router.push('/score');
}
</script>

<style lang="scss" scoped></style>
