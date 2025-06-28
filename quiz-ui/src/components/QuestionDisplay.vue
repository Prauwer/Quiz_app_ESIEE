<!-- Component des questions  -->
<template>
  <div v-if="currentQuestion">
    <h2>{{ currentQuestion.title }}</h2>
    <p>{{ currentQuestion.text }}</p>
    <img v-if="currentQuestion.image" :src="currentQuestion.image" alt="Image de la question" />
    <ul>
      <li v-for="(answer, index) in currentQuestion.possibleAnswers" :key="answer.id">
        <!-- On envoie l'ID unique de la réponse au lieu de son index -->
        <a @click="handleAnswerClick(answer.id)">{{ answer.text }}</a>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  currentQuestion: Object,
});

const emit = defineEmits(["answer-clicked"]);

// La fonction émet maintenant l'ID de la réponse cliquée
function handleAnswerClick(answerId) {
  emit("answer-clicked", answerId);
}
</script>

<style lang="css" scoped>
li a {
  cursor: pointer;
}

/* Style pour l'image de la question */
img {
  display: block; /* Nécessaire pour que margin: auto fonctionne */
  max-width: 50%; /* L'image prendra au maximum 50% de la largeur de son conteneur */
  height: auto; /* La hauteur s'ajuste pour conserver les proportions */
  margin: 20px auto; /* Ajoute 20px d'espace en haut/bas et centre l'image horizontalement */
  border-radius: 8px; /* Ajoute des bords arrondis pour un aspect plus moderne */
}
</style>
