<template>
  <div class="card shadow-sm questions-list">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h3 class="h5 mb-0">Liste des Questions ({{ questions.length }})</h3>
      <router-link to="/admin/edit/new" class="button">Ajouter une question</router-link>
    </div>

    <ul class="list-group list-group-flush">
      <li
        v-for="question in questions"
        :key="question.id"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <span>{{ question.position }}. {{ question.title }}</span>
        <div class="actions">
          <router-link :to="'/admin/edit/' + question.id" class="button-edit">Modifier</router-link>
          <button @click="deleteQuestion(question.id)" class="button-delete">Supprimer</button>
        </div>
      </li>
    </ul>

    <div class="card-footer bg-danger-subtle text-danger-emphasis">
      <h4 class="h6 mb-2">Actions globales (irréversibles)</h4>
      <button @click="deleteAllQuestions" class="btn btn-danger btn-sm me-2">
        Supprimer toutes les questions
      </button>
      <button @click="deleteAllParticipations" class="btn btn-danger btn-sm">
        Supprimer toutes les participations
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService.js';

const questions = ref([]);

async function loadQuestions() {
  try {
    const info = await quizApiService.getQuizInfo();
    const promises = [];
    for (let i = 1; i <= info.data.size; i++) {
      promises.push(quizApiService.getQuestionByPosition(i));
    }
    const responses = await Promise.all(promises);
    questions.value = responses.map((res) => res.data).sort((a, b) => a.position - b.position);
  } catch (e) {
    console.error("Erreur lors du chargement des questions pour l'admin:", e);
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

async function deleteAllQuestions() {
  if (
    window.confirm(
      'ACTION IRRÉVERSIBLE !\nÊtes-vous sûr de vouloir supprimer TOUTES les questions ?'
    )
  ) {
    try {
      await quizApiService.deleteAllQuestions();
      alert('Toutes les questions ont été supprimées.');
      loadQuestions(); // Recharger la liste pour la vider
    } catch (error) {
      alert('La suppression de toutes les questions a échoué.');
    }
  }
}

async function deleteAllParticipations() {
  if (
    window.confirm(
      'ACTION IRRÉVERSIBLE !\nÊtes-vous sûr de vouloir supprimer TOUTES les participations ?'
    )
  ) {
    try {
      await quizApiService.deleteAllParticipations();
      alert('Toutes les participations ont été supprimées.');
    } catch (error) {
      alert('La suppression de toutes les participations a échoué.');
    }
  }
}
</script>

<style scoped>
.actions {
  display: flex;
  gap: 10px;
}

.button,
.button-edit,
.button-delete {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
  color: white;
  font-weight: bold;
  text-align: center;
  display: inline-block;
}
.button {
  background-color: #198754; /* Vert Bootstrap */
}
.button-edit {
  background-color: #ffc107; /* Jaune Bootstrap */
  color: #000;
}
.button-delete {
  background-color: #dc3545; /* Rouge Bootstrap */
}
</style>
