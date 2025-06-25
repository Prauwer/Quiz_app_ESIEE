<template>
  saisissez votre nom et prénom pour démarrer le quiz
  <form @submit.prevent="launchNewQuiz">
    <input type="text" v-model="username" placeholder="Prenom NOM" />
    <button type="submit">Démarrer le quiz</button>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService.js';

const username = ref('');
const router = useRouter();

function launchNewQuiz() {
  console.log('Launch new quiz with', username.value);
  if (username.value.trim() === '') {
    alert('Veuillez saisir votre nom et prénom.');
    return;
  }
  participationStorageService.savePlayerName(username.value);
  router.push('/questions');
}
</script>

<style lang="scss" scoped></style>
