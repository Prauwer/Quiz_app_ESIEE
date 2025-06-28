<template>
  <div v-if="currentQuestion" class="text-center">
    <h2 class="h3 mb-3">{{ currentQuestion.title }}</h2>
    <p class="lead text-muted">{{ currentQuestion.text }}</p>

    <img
      v-if="currentQuestion.image"
      :src="currentQuestion.image"
      alt="Image de la question"
      class="img-fluid rounded shadow-sm my-4"
    />

    <div class="list-group mt-4">
      <a
        v-for="(answer, index) in currentQuestion.possibleAnswers"
        :key="answer.id"
        @click="handleAnswerClick(index + 1)"
        class="list-group-item list-group-item-action fs-5"
      >
        {{ answer.text }}
      </a>
    </div>
  </div>
</template>

<script setup>
defineProps({
  currentQuestion: Object,
});

const emit = defineEmits(['answer-clicked']);

function handleAnswerClick(answerId) {
  emit('answer-clicked', answerId);
}
</script>

<style lang="css" scoped>
.list-group-item-action {
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}
.list-group-item-action:hover,
.list-group-item-action:focus {
  transform: scale(1.02);
  background-color: #f8f9fa;
  border-color: #0d6efd;
  /* [AJOUT] Restaure la bordure supérieure au survol pour tous les éléments */
  border-top-width: 1px;
  color: #0d6efd;
  z-index: 1;
}
img {
  max-height: 400px;
  width: auto;
  max-width: 100%;
}
</style>
