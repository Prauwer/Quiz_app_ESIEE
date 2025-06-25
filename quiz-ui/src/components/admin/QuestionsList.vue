<template>
  <div class="questions-list">
    <div class="list-header">
      <h3>Liste des Questions ({{ questions.length }})</h3>
      <router-link to="/admin/edit/new" class="button">Ajouter une question</router-link>
    </div>
    <ul>
      <li v-for="question in questions" :key="question.id">
        <span>{{ question.title }}</span>
        <div class="actions">
          <router-link :to="'/admin/edit/' + question.id" class="button-edit">Modifier</router-link>
          <button @click="deleteQuestion(question.id)" class="button-delete">Supprimer</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import quizData from '@/data/questions.json';

const questions = ref(quizData.questions);

function deleteQuestion(questionId) {
  // PENSEZ A L'ERGONOMIE : on demande confirmation !
  if (window.confirm('Êtes-vous sûr de vouloir supprimer cette question ?')) {
    console.log(`SIMULATION : Suppression de la question avec l'ID ${questionId}`);
    // NOTE : On ne peut pas modifier le fichier JSON directement.
    // L'API s'en chargera. Pour la simulation, on pourrait filtrer la liste locale.
    questions.value = questions.value.filter((q) => q.id !== questionId);
    alert('Question supprimée (simulation).');
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
