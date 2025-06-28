<template>
  <div class="questions-list">
    <div class="list-header">
      <h3>Liste des Questions ({{ questions.length }})</h3>
      <router-link to="/admin/edit/new" class="button">Ajouter une question</router-link>
    </div>
    <ul>
      <li v-for="question in questions" :key="question.id">
        <span>{{ question.position }}. {{ question.title }}</span>
        <div class="actions">
          <router-link :to="'/admin/edit/' + question.id" class="button-edit">Modifier</router-link>
          <button @click="deleteQuestion(question.id)" class="button-delete">Supprimer</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService.js';

const questions = ref([]);

async function loadQuestions() {
  // Note: l'admin a aussi besoin de toutes les questions.
  // En attendant, on utilise la même logique de boucle que pour les participants.
  try {
    const info = await quizApiService.getQuizInfo();
    const promises = [];
    for (let i = 1; i <= info.data.size; i++) {
      promises.push(quizApiService.getQuestionByPosition(i));
    }
    const responses = await Promise.all(promises);
    questions.value = responses.map((res) => res.data).sort((a, b) => a.position - b.position);
  } catch (e) {
    console.error('Erreur chargement questions admin', e);
  }
}

onMounted(loadQuestions);

async function deleteQuestion(questionId) {
  if (window.confirm('Êtes-vous sûr de vouloir supprimer cette question ?')) {
    try {
      await quizApiService.deleteQuestion(questionId);
      loadQuestions(); // Recharger la liste
    } catch (error) {
      alert('La suppression a échoué.');
    }
  }
}
</script>

<style scoped>
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}
.actions {
  display: flex;
  gap: 10px;
}
</style>
