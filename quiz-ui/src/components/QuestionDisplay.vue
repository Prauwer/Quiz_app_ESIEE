<!-- Component des questions  -->
<template>
  <div v-if="currentQuestion">
    <h2>{{ currentQuestion.title }}</h2>
    <p>{{ currentQuestion.text }}</p>
    <img v-if="currentQuestion.image" :src="currentQuestion.image" alt="Image de la question" />
    <ul>
      <li v-for="(answer, index) in currentQuestion.possibleAnswers" :key="answer.id">
        <a @click="handleAnswerClick(index + 1)">{{ answer.text }}</a>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  currentQuestion: Object,
});

const emit = defineEmits(['answer-clicked']);

function handleAnswerClick(index) {
  emit('answer-clicked', index);
}
</script>

<style lang="css" scoped>
li a {
  cursor: pointer;
}
</style>
