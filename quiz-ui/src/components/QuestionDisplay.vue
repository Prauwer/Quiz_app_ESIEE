<!-- Component des questions  -->
<template>
  <div v-if="currentQuestion">
    <h2>{{ currentQuestion.title }}</h2>
    <img v-if="currentQuestion.image" :src="currentQuestion.image" alt="Image de la question" />

    <ul>
      <li v-for="(answer, index) in currentQuestion.propositions" :key="index">
        <a @click="handleAnswerClick(index)">{{ answer }}</a>
      </li>
    </ul>
  </div>
</template>

<script setup>
const props = defineProps({
  currentQuestion: Object,
});

const emit = defineEmits(['answer-clicked']);

function handleAnswerClick(index) {
  emit('answer-clicked', index);
}
</script>

<style lang="css" scoped></style>
