<template>
  <p>Saisissez votre nom et prénom pour démarrer le quiz</p>
  <form @submit.prevent="launchNewQuiz">
    <input type="text" v-model="username" placeholder="Prenom NOM" required />
    <button type="submit">Démarrer le quiz</button>
  </form>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService.js';

const username = ref('');
const router = useRouter();

function launchNewQuiz() {
  if (username.value.trim() === '') return;
  participationStorageService.savePlayerName(username.value);
  router.push('/questions');
}
</script>

<style lang="scss" scoped></style>
